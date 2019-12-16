import os
import json

path_to_json = os.path.join('.', 'cookiecutter.json')

def test_json_exists():
    assert os.path.exists(path_to_json)


def test_json_data_structure():
    with open(path_to_json) as f:
        cc_dict = json.load(f)
    assert isinstance(cc_dict, dict)

def test_loop_structure():
    with open(path_to_json) as f:
        cc_dict = json.load(f)
    for key, value in cc_dict.items():
        if key.startswith('loop_'):
            assert isinstance(value, dict)
            assert isinstance(value.get('default', 1), int)
            for k, v in value.items():
                if k.startswith('loop_'):
                    assert isinstance(v, dict)
                    assert isinstance(v.get('default', 1), int)
                if k.endswith('_iter'):
                    assert isinstance(v, str)
