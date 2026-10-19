from tools.checks import version_check


def cf(filename, pid, fid, side="both"):
    return {"filename": filename, "side": side, "update": {"curseforge": {"project-id": pid, "file-id": fid}}}


METAS = {
    "jei": cf("jei.jar", 1, 10),
    "sodium": cf("sodium.jar", 2, 20, side="client"),
    "servus-alchemy": {"filename": "alchemy.jar", "side": "both", "download": {"mode": "url"}},
}
MANIFEST = {"files": [{"projectID": 1, "fileID": 10}, {"projectID": 2, "fileID": 20}]}


def test_matching_build_passes():
    assert version_check.check(METAS, MANIFEST, {"jei.jar", "alchemy.jar"}) == []


def test_client_only_jar_in_server_pack_fails():
    errors = version_check.check(METAS, MANIFEST, {"jei.jar", "alchemy.jar", "sodium.jar"})
    assert errors == ["sodium: client-only jar sodium.jar is in the server pack"]


def test_different_file_in_manifest_fails():
    manifest = {"files": [{"projectID": 1, "fileID": 11}, {"projectID": 2, "fileID": 20}]}
    errors = version_check.check(METAS, manifest, {"jei.jar", "alchemy.jar"})
    assert errors == ["jei: manifest has file 11, metafile has 10"]


def test_missing_and_unknown_jars_fail():
    errors = version_check.check(METAS, MANIFEST, {"alchemy.jar", "jei-old.jar"})
    assert errors == ["jei: jei.jar is missing from the server pack",
                      "server pack has a jar no metafile describes: jei-old.jar"]
