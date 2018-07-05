def merge_dict(source, other):
    if not isinstance(source, dict):
        raise TypeError("Merge dict received {} as first argument, expecting dict".format(type(source))) 
    if not isinstance(other, dict):
        raise TypeError("Merge dict received {} as second argument, expecting dict".format(type(other))) 
    for k, v in other.items():
        if k in source:
            merge_dict(source[k], v)
        else:
            source[k] = v