from os import path
from pathlib import Path

def _optionally_typed(obj, optional_type=None):
    if optional_type is not None:
        return optional_type(obj)
    else:
        return obj

def get_input(prompt, input_type=None, default=None):
    while True:
        user_input = input(prompt)
        if user_input:
            return _optionally_typed(user_input, input_type)
        if default is not None:
            return _optionally_typed(default, input_type)

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

def get_yn(prompt, default=None):
    if default is None:
        prompt += ' y/n: '
    elif default:
        prompt += ' [y]/n: '
    else:
        prompt += ' y/[n]: '
    while True:
        user_input = input(prompt)
        if user_input.lower() in ['y', 'yes']:
            return True
        elif user_input.lower() in ['n', 'no']:
            return False
        elif default is not None:
            return bool(default)

def propose_next_action():
    print("Successfully generated terraform files, please run the following command to view the proposed changes:")
    print("\n> terraform init && terraform plan\n")

    print("If everything looks right, run:")
    print("\n> terraform apply\n")