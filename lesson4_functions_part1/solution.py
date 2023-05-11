def recursive_search(src: dict, value: str, deep=-1, parent=None):
    if isinstance(src, dict):
        deep += 1
        for k, v in src.items():
            recursive_search(v, value, deep=deep, parent=k)
    elif isinstance(src, list):
        for item in src:
            recursive_search(item, value, deep=deep, parent=parent)
    elif isinstance(src, str):
        if src == value:
            print(f'Found "{value}" on deep = {deep}, parent = {parent}')
            return src
