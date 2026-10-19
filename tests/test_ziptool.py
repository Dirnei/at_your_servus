import json
import zipfile

from tools import ziptool


def test_profile_image_is_added_and_referenced(tmp_path):
    pack = tmp_path / "pack.zip"
    with zipfile.ZipFile(pack, "w") as z:
        z.writestr("manifest.json", json.dumps({"name": "Servus", "files": []}))
        z.writestr("overrides/config/a.toml", "x = 1")
    image = tmp_path / "logo.png"
    image.write_bytes(b"png")
    ziptool.set_profile_image(pack, image)
    ziptool.set_profile_image(pack, image)  # a second run replaces, not duplicates
    with zipfile.ZipFile(pack) as z:
        names = z.namelist()
        manifest = json.loads(z.read("manifest.json"))
        assert z.read("profileImage/logo.png") == b"png"
    assert names.count("profileImage/logo.png") == 1
    assert "overrides/config/a.toml" in names
    assert manifest == {"name": "Servus", "files": [], "image": "profileImage/logo.png"}
