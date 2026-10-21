import subprocess

from tools import changelog


def git(repo, *args):
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)


def metafile(repo, path, name, filename):
    (repo / path).parent.mkdir(parents=True, exist_ok=True)
    (repo / path).write_bytes(f'name = "{name}"\nfilename = "{filename}"\nside = "both"\n'.encode())


def commit(repo, message):
    git(repo, "add", "-A")
    git(repo, "commit", "--allow-empty", "-q", "-m", message)


def released_repo(tmp_path):
    git(tmp_path, "init", "-q")
    git(tmp_path, "config", "user.email", "t@example.com")
    git(tmp_path, "config", "user.name", "t")
    metafile(tmp_path, "mods/servus-shuttles.pw.toml", "Servus: Shuttles", "servus_shuttles-0.1.0-beta.jar")
    metafile(tmp_path, "mods/old.pw.toml", "Old Mod", "old-1.0.jar")
    metafile(tmp_path, "mods/jei.pw.toml", "JEI", "jei-1.jar")
    commit(tmp_path, "Initial pack")
    git(tmp_path, "tag", "v0.1.0-alpha")
    return tmp_path


def test_draft_groups_commits_and_lists_mod_changes(tmp_path):
    repo = released_repo(tmp_path)
    metafile(repo, "mods/servus-shuttles.pw.toml", "Servus: Shuttles", "servus_shuttles-0.2.0.jar")
    metafile(repo, "shaderpacks/complementary-reimagined.pw.toml", "Complementary Reimagined", "ComplementaryReimagined_r5.9.3.zip")
    (repo / "mods/old.pw.toml").unlink()
    commit(repo, "feat: add FTB Essentials with /rtp off")
    commit(repo, "chore(tools): add client-sync.ps1")
    commit(repo, "fix(quests): keep the seeds quest open")
    text = changelog.draft(repo, "0.2.0-alpha")
    assert text.startswith("## 0.2.0-alpha\n")
    assert "### New\n\n- Add FTB Essentials with /rtp off\n" in text
    assert "### Fixes\n\n- Keep the seeds quest open\n" in text
    assert "client-sync" not in text and "### Performance" not in text
    mods = text.split("### Mods\n\n")[1]
    assert mods.splitlines()[:3] == [
        "- Added: Complementary Reimagined (`ComplementaryReimagined_r5.9.3.zip`)",
        "- Removed: Old Mod (`old-1.0.jar`)",
        "- Updated: Servus: Shuttles (`servus_shuttles-0.1.0-beta.jar` to `servus_shuttles-0.2.0.jar`)",
    ]
    assert "JEI" not in text


def test_commits_count_from_the_tag_before_an_existing_version_tag(tmp_path):
    repo = released_repo(tmp_path)
    commit(repo, "feat: add shaders")
    git(repo, "tag", "v0.2.0-alpha")
    assert "- Add shaders" in changelog.draft(repo, "0.2.0-alpha")


def test_empty_groups_are_left_out(tmp_path):
    repo = released_repo(tmp_path)
    commit(repo, "docs: explain the dev client")
    assert changelog.draft(repo, "0.2.0-alpha") == "## 0.2.0-alpha\n"


def test_main_inserts_newest_first_and_refuses_twice(tmp_path, capsys):
    repo = released_repo(tmp_path)
    (repo / "CHANGELOG.md").write_bytes(b"# Changelog\n\n## 0.1.0-alpha\n\n- First release\n")
    commit(repo, "feat: add shaders")
    assert changelog.main(["0.2.0-alpha", "--root", str(repo)]) == 0
    text = (repo / "CHANGELOG.md").read_text(encoding="utf-8")
    assert text.index("## 0.2.0-alpha") < text.index("## 0.1.0-alpha")
    assert text.startswith("# Changelog\n\n## 0.2.0-alpha\n")
    assert changelog.main(["0.2.0-alpha", "--root", str(repo)]) == 1
    assert "already has a section for 0.2.0-alpha" in capsys.readouterr().err
    assert (repo / "CHANGELOG.md").read_text(encoding="utf-8") == text


def test_main_creates_the_file(tmp_path):
    repo = released_repo(tmp_path)
    commit(repo, "feat: add shaders")
    assert changelog.main(["0.2.0-alpha", "--root", str(repo)]) == 0
    assert (repo / "CHANGELOG.md").read_text(encoding="utf-8") == "# Changelog\n\n## 0.2.0-alpha\n\n### New\n\n- Add shaders\n"
