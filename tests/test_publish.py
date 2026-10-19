import pytest

from tools import publish


def test_version_comes_from_the_tag():
    assert publish.version_from_tag("v0.1.0") == "0.1.0"
    assert publish.version_from_tag("v0.1.0-alpha") == "0.1.0-alpha"
    assert publish.version_from_tag("v0.2.0-beta.2") == "0.2.0-beta.2"
    for bad in ["0.1.0", "v0.1", "v0.1.0-rc1", "v0.1.0.1", "release"]:
        with pytest.raises(publish.PublishError, match="not a release tag"):
            publish.version_from_tag(bad)


def test_release_type_follows_version_suffix():
    assert publish.release_type("0.1.0-alpha") == "alpha"
    assert publish.release_type("0.2.0-beta.2") == "beta"
    assert publish.release_type("0.1.0") == "release"


def test_check_prints_the_version(capsys):
    assert publish.main(["--tag", "v0.1.0-alpha", "--check"]) == 0
    assert capsys.readouterr().out.strip() == "0.1.0-alpha"


def test_missing_configuration_uploads_nothing(tmp_path, monkeypatch, capsys):
    monkeypatch.delenv("CF_PROJECT_ID", raising=False)
    monkeypatch.setenv("CF_API_TOKEN", "secret-token")
    monkeypatch.setattr(publish, "upload", lambda *a: pytest.fail("must not upload"))
    assert publish.main(["--tag", "v0.1.0", "--root", str(tmp_path)]) == 0
    out = capsys.readouterr().out
    assert "CF_PROJECT_ID" in out and "secret-token" not in out


def test_bad_tag_fails_before_upload(tmp_path, monkeypatch):
    monkeypatch.setenv("CF_PROJECT_ID", "1")
    monkeypatch.setenv("CF_API_TOKEN", "t")
    monkeypatch.setattr(publish, "upload", lambda *a: pytest.fail("must not upload"))
    assert publish.main(["--tag", "nightly", "--root", str(tmp_path)]) == 1
