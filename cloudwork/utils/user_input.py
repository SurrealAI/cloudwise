from os import path
from pathlib import Path

def optionally_typed(obj, optional_type=None)
    if optional_type is not None:
        return optional_type(obj)
    else:
        return obj

def get_input(prompt, input_type=None, default=None):
    while True:
        user_input = input(prompt)
        if user_input:
            return optionally_typed(user_input, input_type)
        if default is not None:
            return optionally_typed(default, input_type)

def get_file(prompt):
    while True:
        file_path = input(prompt)
        if not file_path:
            continue
        file = Path(path.expanduser(file_path))
        if file.exists():
            return str(file)
        else:
            print('Cannot find file {}'.format(file_path))
