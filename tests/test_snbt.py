import pytest

from tools.questgen.snbt import Byte, Double, Long, dump_file, dumps, quote


def test_scalars():
    assert dumps(True) == "true"
    assert dumps(3) == "3"
    assert dumps(Double(1)) == "1.0d"
    assert dumps(-2.5) == "-2.5d"
    assert dumps(Long(7)) == "7L"
    assert dumps(Byte(1)) == "1b"


def test_string_escaping():
    assert quote('say "Servus"\\\nnext') == '"say \\"Servus\\"\\\\\\nnext"'


def test_compound_sorted_keys_and_tabs():
    assert dumps({"b": 1, "a": {"x": "y"}}) == '{\n\ta: {\n\t\tx: "y"\n\t}\n\tb: 1\n}'


def test_lists_and_empty_values():
    assert dumps([1, 2]) == "[\n\t1\n\t2\n]"
    assert dumps([]) == "[ ]"
    assert dumps({}) == "{ }"


def test_keys_needing_quotes():
    assert dumps({"quest.ABC.title": "x", "a b": 1}) == '{\n\t"a b": 1\n\tquest.ABC.title: "x"\n}'


def test_file_ends_with_newline_and_is_stable():
    data = {"z": [Double(0.5)], "id": "0123456789ABCDEF"}
    assert dump_file(data) == dump_file(dict(reversed(list(data.items()))))
    assert dump_file(data).endswith("}\n")


def test_unknown_type_fails():
    with pytest.raises(TypeError):
        dumps(object())
