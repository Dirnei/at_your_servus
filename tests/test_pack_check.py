from tools.checks import pack_check


def cf(pid, side="both"):
    return {"side": side, "update": {"curseforge": {"project-id": pid, "file-id": 1}}}


def with_filename(meta, filename):
    return {**meta, "filename": filename}


def url(side="both"):
    return {"side": side, "download": {"mode": "url", "url": "https://example.invalid/a.jar"}}


def complete():
    metas = {slug: cf(1000 + i) for i, slug in enumerate(pack_check.REQUIRED_SLUGS)}
    metas["servus-alchemy"] = url()
    for i, slug in enumerate(pack_check.CLIENT_ONLY_SLUGS):
        metas[slug] = cf(2000 + i, side="client")
    metas["euphoria-patches"]["filename"] = "EuphoriaPatcher-1.10.5-r5.9.3-neoforge.jar"
    return metas


def test_complete_pack_passes():
    assert pack_check.check(complete()) == []


def test_excluded_project_fails_and_names_mod():
    metas = complete()
    metas["ae2"] = cf(223794)
    assert pack_check.check(metas) == ["excluded mod Applied Energistics 2 is in the pack (ae2)"]


def test_shader_pack_for_both_sides_fails_and_is_named():
    shaders = {"complementary-reimagined": with_filename(cf(3000, side="both"), "ComplementaryReimagined_r5.9.3.zip")}
    assert pack_check.check(complete(), shaders=shaders) == [
        "shader pack complementary-reimagined must be side = \"client\", is 'both'"]


def test_public_fails_on_url_shader_pack():
    metas = complete()
    metas["servus-alchemy"] = cf(1999)
    errors = pack_check.check(metas, public=True, shaders={"some-shader": url(side="client")})
    assert errors == ["some-shader is not sourced from CurseForge; switch it to CurseForge before a public build"]


def test_euphoria_patches_matching_complementary_passes():
    metas = complete()
    shaders = {"complementary-reimagined": with_filename(cf(3000, side="client"), "ComplementaryReimagined_r5.9.3.zip"),
               "complementary-unbound": with_filename(cf(3001, side="client"), "ComplementaryUnbound_r5.9.3.zip")}
    assert pack_check.check(metas, shaders=shaders) == []


def test_euphoria_patches_version_mismatch_fails_and_names_files():
    metas = complete()
    shaders = {"complementary-unbound": with_filename(cf(3001, side="client"), "ComplementaryUnbound_r5.10.0.zip")}
    assert pack_check.check(metas, shaders=shaders) == [
        "Euphoria Patches and Complementary are built for different versions: "
        "EuphoriaPatcher-1.10.5-r5.9.3-neoforge.jar, ComplementaryUnbound_r5.10.0.zip"]


def test_complementary_without_version_fails():
    metas = complete()
    shaders = {"complementary-unbound": with_filename(cf(3001, side="client"), "ComplementaryUnbound.zip")}
    assert pack_check.check(metas, shaders=shaders) == [
        "ComplementaryUnbound.zip names no Complementary version (r<version>)"]


def test_missing_required_mod_fails():
    metas = complete()
    del metas["powah-rearchitected"]
    assert pack_check.check(metas) == ["required mod powah-rearchitected is missing"]


def test_client_only_mod_with_wrong_side_fails():
    metas = complete()
    metas["sodium"]["side"] = "both"
    assert pack_check.check(metas) == ["sodium must be side = \"client\", is 'both'"]


def test_example_export_mod_missing_fails():
    errors = pack_check.check(complete(), example_ids={1000, 999999})
    assert errors == ["mod from Servus-0.1.0.zip is missing (CurseForge project 999999)"]


def test_public_fails_on_url_mod_but_playtest_passes():
    metas = complete()
    assert pack_check.check(metas, public=False) == []
    errors = pack_check.check(metas, public=True)
    assert errors == ["servus-alchemy is not sourced from CurseForge; switch it to CurseForge before a public build"]


def test_every_metafile_is_documented():
    import re
    from pathlib import Path
    root = Path(__file__).resolve().parent.parent
    documented = set(re.findall(r"^\| `([a-z0-9-]+)` \|", (root / "docs/mods.md").read_text(encoding="utf-8"), re.M))
    mods, shaders = pack_check.load_pack(root)
    metafiles = set(mods) | set(shaders)
    assert metafiles - documented == set(), "metafiles without an entry in docs/mods.md"
    assert documented - metafiles == set(), "docs/mods.md entries without a metafile"
