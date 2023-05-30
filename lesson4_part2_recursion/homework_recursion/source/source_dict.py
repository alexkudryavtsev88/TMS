def get_source_dict():
    return {
        "key1": "John",  # deep 0
        'key2': {
            'key3': 'Alex',  # deep 1
            'key4': {
                'key5': ['Kate', 'Mary'],  # deep 2
                'key6': {
                    'key7': [
                        'Bob',  # deep 3
                        'Duke',
                        {
                            'key8': {  # deep 4
                                'key9': [  # deep 5
                                    'Lisa',
                                    {
                                        'key10': ['Mark']  # deep 6
                                    }
                                ]
                            }
                        }
                    ]
                },
            },
            'key8': 'Robert'  # deep 1
        }
    }


""" Пример словаря c дубликатами: """
def get_source_dict_with_duplicates():
    return {
        "key1": {
            "key2": {
                "key3": [
                    "John",
                    {
                        "key4": "Bob",
                        "key5": "Alex",
                        "key6": {
                            "key7": [
                                {
                                    "key7": "Jessica",
                                    "key8": {
                                        "key9": [
                                            "Alex"
                                        ]
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        },
        "key4": "Kate"
    }
