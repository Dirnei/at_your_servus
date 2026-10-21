import pytest

from tools import publish

CHANGELOG = "# Changelog\n\n## 0.2.0-alpha\n\n### New\n\n- Add shaders\n\n## 0.1.0-alpha\n\n- First release\n"


@pytest.fixture
def root(tmp_path):
    (tmp_path / "CHANGELOG.md").write_bytes(CHANGELOG.encode())
    return tmp_path


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


def test_changelog_section_ends_at_the_next_version(root):
    assert publish.changelog_section(root, "0.2.0-alpha") == "### New\n\n- Add shaders"
    assert publish.changelog_section(root, "0.1.0-alpha") == "- First release"


def test_check_prints_the_version(root, capsys):
    assert publish.main(["--tag", "v0.2.0-alpha", "--check", "--root", str(root)]) == 0
    assert capsys.readouterr().out.strip() == "0.2.0-alpha"


def test_check_fails_without_a_section(root, capsys):
    assert publish.main(["--tag", "v0.3.0-alpha", "--check", "--root", str(root)]) == 1
    assert "no section ## 0.3.0-alpha" in capsys.readouterr().err


def test_check_fails_on_an_empty_section(tmp_path, capsys):
    (tmp_path / "CHANGELOG.md").write_bytes(b"# Changelog\n\n## 0.2.0-alpha\n\n## 0.1.0-alpha\n\n- First release\n")
    assert publish.main(["--tag", "v0.2.0-alpha", "--check", "--root", str(tmp_path)]) == 1
    assert "## 0.2.0-alpha is empty" in capsys.readouterr().err


def test_client_upload_carries_the_changelog(root, monkeypatch):
    monkeypatch.setenv("CF_PROJECT_ID", "1")
    monkeypatch.setenv("CF_API_TOKEN", "t")
    monkeypatch.setattr(publish, "game_version_id", lambda token: 7)
    uploads = []
    monkeypatch.setattr(publish, "upload", lambda pid, token, file, meta: uploads.append((file.name, meta)) or 99)
    assert publish.main(["--tag", "v0.2.0-alpha", "--root", str(root)]) == 0
    (client, client_meta), (server, server_meta) = uploads
    assert client == "at-your-servus-0.2.0-alpha.zip" and client_meta["changelog"] == "### New\n\n- Add shaders"
    assert server_meta["changelog"] == "Server pack for At Your Servus 0.2.0-alpha" and server_meta["parentFileID"] == 99


def test_missing_configuration_uploads_nothing(root, monkeypatch, capsys):
    monkeypatch.delenv("CF_PROJECT_ID", raising=False)
    monkeypatch.setenv("CF_API_TOKEN", "secret-token")
    monkeypatch.setattr(publish, "upload", lambda *a: pytest.fail("must not upload"))
    assert publish.main(["--tag", "v0.2.0-alpha", "--root", str(root)]) == 0
    out = capsys.readouterr().out
    assert "CF_PROJECT_ID" in out and "secret-token" not in out


def test_bad_tag_fails_before_upload(root, monkeypatch):
    monkeypatch.setenv("CF_PROJECT_ID", "1")
    monkeypatch.setenv("CF_API_TOKEN", "t")
    monkeypatch.setattr(publish, "upload", lambda *a: pytest.fail("must not upload"))
    assert publish.main(["--tag", "nightly", "--root", str(root)]) == 1
