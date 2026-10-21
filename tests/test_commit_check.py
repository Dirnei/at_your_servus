import subprocess

from tools.checks import commit_check


def problem(message):
    return commit_check.problem(message)


def test_conventional_commit_passes():
    assert problem("feat: add FTB Essentials with /rtp off") is None
    assert problem("chore(tools): add client-sync.ps1") is None
    assert problem("fix!: keep homes after a restart") is None


def test_every_known_type_passes():
    for t in commit_check.TYPES:
        assert problem(f"{t}: something") is None


def test_leading_space_fails():
    assert "not a conventional commit" in problem(" chore(tools): add the quest explorer")


def test_unknown_type_fails():
    assert "not a conventional commit" in problem("feature: add shaders")
    assert "not a conventional commit" in problem("Add shaders")


def test_too_long_fails():
    message = "feat: " + "x" * 69
    assert len(message) == 75
    assert problem(message) == "75 characters, at most 74"
    assert problem(message[:-1]) is None


def test_body_fails():
    assert problem("feat: add shaders\n\nBecause my wife asked.") == "message must be one line"
    assert problem("feat: add shaders\n") is None


def git(repo, *args):
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)


def commit(repo, message):
    git(repo, "commit", "--allow-empty", "-q", "-m", message)


def repo_with_tag(tmp_path):
    git(tmp_path, "init", "-q")
    git(tmp_path, "config", "user.email", "t@example.com")
    git(tmp_path, "config", "user.name", "t")
    commit(tmp_path, "Old style commit before the release")
    git(tmp_path, "tag", "v0.1.0-alpha")
    return tmp_path


def test_only_commits_since_the_tag_are_checked(tmp_path):
    repo = repo_with_tag(tmp_path)
    commit(repo, "feat: add shaders")
    commit(repo, " chore(tools): add the quest explorer")
    assert commit_check.previous_tag(repo) == "v0.1.0-alpha"
    errors = commit_check.check(commit_check.commits(repo, "v0.1.0-alpha"))
    assert len(errors) == 1 and "quest explorer" in errors[0] and "not a conventional commit" in errors[0]


def test_main_fails_and_names_the_commit(tmp_path, capsys):
    repo = repo_with_tag(tmp_path)
    commit(repo, "feat: " + "x" * 80)
    assert commit_check.main(["--root", str(repo)]) == 1
    assert "86 characters" in capsys.readouterr().out


def test_no_tag_checks_everything(tmp_path):
    git(tmp_path, "init", "-q")
    git(tmp_path, "config", "user.email", "t@example.com")
    git(tmp_path, "config", "user.name", "t")
    commit(tmp_path, "Initial commit")
    assert commit_check.previous_tag(tmp_path) is None
    assert len(commit_check.check(commit_check.commits(tmp_path, None))) == 1
