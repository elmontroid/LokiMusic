from typing import Any, Dict


def parse(value : str) -> Any:
    value = value.strip()

    if value.isdigit(): return int(value)
    if value.replace(".", "", 1).isdigit(): return float(value)

    if value.lower() == 'false': return False
    if value.lower() == 'true':  return True
    if value.lower() == 'none':  return None

    if value.startswith('[') and value.endswith(']'): return parseList(value)
    if value.startswith('{') and value.endswith('}'): return parseDict(value)

    if value.startswith('"') and value.endswith('"'): value = value.split('"')[1]
    if value.startswith("'") and value.endswith("'"): value = value.split("'")[1]

    return value


def parseList(document : list[str] | str) -> list:

    slices = []
    document = str(document)[1:-1]

    for item in document.split(','):
        slices.append(parse(item))

    return slices


def parseDict(document : Dict[str, Any] | str) -> Dict[str, Any]:

    dictionary = {}
    document = str(document)[1:-1]

    for item in document.split(','):
        dictionary[item.split(':')[0]] = parse(item.split(':')[1])

    return dictionary
