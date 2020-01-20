def popconvert(obj, key, convert=None):
    value = obj.pop(key, None)
    if isinstance(value, dict) and convert:
        return convert(**value)
    return convert(value) if value and convert else value
