import pytest

from tools import publish


def test_tag_must_match_version():
    publish.check_tag("v0.1.0", "0.1.0")
    with pytest.raises(publish.PublishError, match="does not match"):
        publish.check_tag("v0.2.0", "0.1.0")


def test_release_type_follows_version_suffix():
    assert publish.release_type("0.1.0-alpha") == "alpha"
    assert publish.release_type("0.2.0-beta.2") == "beta"
    assert publish.release_type("0.1.0") == "release"


def test_missing_configuration_uploads_nothing(tmp_path, monkeypatch, capsys):
    (tmp_path / "pack.toml").write_text('version = "0.1.0"\n', encoding="utf-8")
    monkeypatch.delenv("CF_PROJECT_ID", raising=False)
    monkeypatch.setenv("CF_API_TOKEN", "secret-token")
    monkeypatch.setattr(publish, "upload", lambda *a: pytest.fail("must not upload"))
    assert publish.main(["--tag", "v0.1.0", "--root", str(tmp_path)]) == 0
    out = capsys.readouterr().out
    assert "CF_PROJECT_ID" in out and "secret-token" not in out


def test_mismatched_tag_fails_before_upload(tmp_path, monkeypatch):
    (tmp_path / "pack.toml").write_text('version = "0.1.0"\n', encoding="utf-8")
    monkeypatch.setenv("CF_PROJECT_ID", "1")
    monkeypatch.setenv("CF_API_TOKEN", "t")
    monkeypatch.setattr(publish, "upload", lambda *a: pytest.fail("must not upload"))
    assert publish.main(["--tag", "v0.2.0", "--root", str(tmp_path)]) == 1
