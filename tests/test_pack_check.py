from tools.checks import pack_check


def cf(pid, side="both"):
    return {"side": side, "update": {"curseforge": {"project-id": pid, "file-id": 1}}}


def url(side="both"):
    return {"side": side, "download": {"mode": "url", "url": "https://example.invalid/a.jar"}}


def complete():
    metas = {slug: cf(1000 + i) for i, slug in enumerate(pack_check.REQUIRED_SLUGS)}
    metas["servus-alchemy"] = url()
    for i, slug in enumerate(pack_check.CLIENT_ONLY_SLUGS):
        metas[slug] = cf(2000 + i, side="client")
    return metas


def test_complete_pack_passes():
    assert pack_check.check(complete()) == []


def test_excluded_project_fails_and_names_mod():
    metas = complete()
    metas["ae2"] = cf(223794)
    assert pack_check.check(metas) == ["excluded mod Applied Energistics 2 is in the pack (ae2)"]


def test_excluded_slug_fails():
    metas = complete()
    metas["iris"] = url(side="client")
    assert any("Iris" in e for e in pack_check.check(metas))


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
