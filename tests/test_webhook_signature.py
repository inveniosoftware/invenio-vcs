# SPDX-FileCopyrightText: 2026 CERN.
# SPDX-License-Identifier: MIT

"""Test the verification of incoming webhook requests."""

import base64
import hashlib
import hmac
import json
import time

import pytest
from invenio_webhooks.errors import InvalidSignature
from invenio_webhooks.models import Event

from invenio_vcs.config import get_provider_by_id
from invenio_vcs.contrib.gitlab import GitLabProvider

SECRET = "s3cret"
BODY = json.dumps({"action": "published"})
JSON = ("Content-Type", "application/json")


def _github_signature(body, secret, prefix="sha256="):
    digest = hmac.new(secret.encode(), body.encode(), hashlib.sha256).hexdigest()
    return [JSON, ("X-Hub-Signature-256", prefix + digest)]


# (provider id, name of the secret in the provider config, valid headers, bad headers)
PROVIDERS = [
    (
        "github",
        "shared_secret",
        lambda: _github_signature(BODY, SECRET),
        [
            [JSON],  # not signed
            _github_signature(BODY, "other"),  # signed with another secret
            _github_signature("{}", SECRET),  # signature of another body
            _github_signature(BODY, SECRET, prefix="sha1="),  # unsupported algorithm
            _github_signature(BODY, SECRET, prefix=""),  # no algorithm
            [JSON, ("X-Hub-Signature-256", "sha256=é")],  # not ASCII
        ],
    ),
    (
        "gitlab",
        "shared_validation_token",
        lambda: [JSON, ("X-Gitlab-Token", SECRET)],
        [
            [JSON],  # no token
            [JSON, ("X-Gitlab-Token", "other")],  # wrong token
            [JSON, ("X-Gitlab-Token", "")],  # empty token
            [JSON, ("X-Gitlab-Token", "é")],  # not ASCII
        ],
    ),
]


@pytest.fixture(params=PROVIDERS, ids=lambda p: p[0])
def provider(request, app):
    """Provider id, valid headers and bad headers; the secret is set on the provider."""
    provider_id, secret_name, valid_headers, bad_headers = request.param
    config = get_provider_by_id(provider_id).provider_specific_config
    old = config.get(secret_name)
    config[secret_name] = SECRET
    yield provider_id, valid_headers(), bad_headers
    config[secret_name] = old


def _post(app, provider_id, headers):
    with app.test_request_context(headers=headers, data=BODY):
        return Event.create(receiver_id=provider_id)


def test_valid_signature_accepted(app, provider):
    """A request with the right signature or token is accepted."""
    provider_id, valid_headers, _ = provider
    event = _post(app, provider_id, valid_headers)
    assert event.payload == json.loads(BODY)


def test_invalid_signature_rejected(app, provider):
    """Requests with a missing or wrong signature or token are rejected."""
    provider_id, _, bad_headers = provider
    for headers in bad_headers:
        with pytest.raises(InvalidSignature):
            _post(app, provider_id, headers)


@pytest.mark.parametrize("provider_id", ["github", "gitlab"])
def test_no_secret_configured_accepts_unsigned(app, provider_id):
    """Without a configured secret nothing is verified (backwards compatible)."""
    event = _post(app, provider_id, [JSON])
    assert event.payload == json.loads(BODY)


# GitLab signing token ("whsec_" + base64 of a 32 byte key), the recommended option.
SIGNING_TOKEN = "whsec_" + base64.b64encode(b"k" * 32).decode()


def _gitlab_signature(body=BODY, token=SIGNING_TOKEN, message_id="msg_1", age=0):
    timestamp = str(int(time.time()) - age)
    key = base64.b64decode(token[len("whsec_") :])
    message = "{}.{}.{}".format(message_id, timestamp, body).encode()
    digest = hmac.new(key, message, hashlib.sha256).digest()
    return [
        JSON,
        ("webhook-id", message_id),
        ("webhook-timestamp", timestamp),
        ("webhook-signature", "v1," + base64.b64encode(digest).decode()),
    ]


@pytest.fixture()
def gitlab_config(app):
    """The GitLab config, with a signing token and a validation token set."""
    config = get_provider_by_id("gitlab").provider_specific_config
    old = dict(config)
    config["shared_signing_token"] = SIGNING_TOKEN
    config["shared_validation_token"] = SECRET
    yield config
    config.clear()
    config.update(old)


def test_gitlab_signing_token_accepted(app, gitlab_config):
    """A request signed with the signing token is accepted."""
    event = _post(app, "gitlab", _gitlab_signature())
    assert event.payload == json.loads(BODY)


def test_gitlab_one_valid_signature_is_enough(app, gitlab_config):
    """The header can hold several signatures; one valid signature is enough."""
    *headers, (name, valid) = _gitlab_signature()
    headers.append((name, "v1,AAAA " + valid))
    assert _post(app, "gitlab", headers).payload == json.loads(BODY)


@pytest.mark.parametrize(
    "headers",
    [
        [JSON],  # not signed
        _gitlab_signature("{}"),  # signature of another body
        _gitlab_signature(token="whsec_" + base64.b64encode(b"x" * 32).decode()),
        _gitlab_signature(age=3600),  # too old (replay)
        _gitlab_signature(age=-3600),  # too far in the future
        [JSON, ("X-Gitlab-Token", SECRET)],  # the plain token is not enough
        [
            JSON,
            ("webhook-id", "m"),
            ("webhook-timestamp", "now"),
            ("webhook-signature", "v1,AAAA"),
        ],  # timestamp is not a number
        [
            JSON,
            ("webhook-id", "m"),
            ("webhook-timestamp", "\u00b2"),
            ("webhook-signature", "v1,AAAA"),
        ],  # not an ASCII number
        [
            JSON,
            ("webhook-id", "m"),
            ("webhook-timestamp", "1"),
            ("webhook-signature", "v1,\u00e9"),
        ],  # not ASCII
    ],
)
def test_gitlab_signing_token_rejected(app, gitlab_config, headers):
    """With a signing token configured, requests without a valid signature fail."""
    with pytest.raises(InvalidSignature):
        _post(app, "gitlab", headers)


def test_gitlab_hook_data_signing_token(app, monkeypatch):
    """The signing token is sent to GitLab when the hook is created or updated."""
    monkeypatch.setattr(GitLabProvider, "webhook_url", "https://example.org/hook")
    factory = get_provider_by_id("gitlab")
    provider = GitLabProvider(factory, user_id=1)
    config = factory.provider_specific_config

    monkeypatch.setitem(config, "shared_signing_token", "")
    assert "signing_token" not in provider._hook_data

    monkeypatch.setitem(config, "shared_signing_token", SIGNING_TOKEN)
    assert provider._hook_data["signing_token"] == SIGNING_TOKEN
