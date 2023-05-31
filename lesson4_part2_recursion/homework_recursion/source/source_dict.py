def get_source_dict():
    return {
        "key1": "John",  # deep 0
        'key2': {
            'key3': 'Ann',  # deep 1
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
                                        'key10': ['Mark', 'Alex']  # deep 6
                                    }
                                ],
                                "key11": "Louisa",  # deep 5
                            }
                        },
                        "Alex",  # deep 3
                    ]
                },
            },
            'key12': 'Robert'  # deep 1
        },
        "key13": "Ronaldo"  # deep 0
    }


# def get_source_dict_with_duplicates():
#     return {
#         "key1": {
#             "key2": {
#                 "key3": [
#                     "John",
#                     {
#                         "key4": "Bob",
#                         "key5": "Alex",
#                         "key6": {
#                             "key7": [
#                                 {
#                                     "key8": "Jessica",
#                                     "key9": {
#                                         "key10": [
#                                             "Alex"
#                                         ]
#                                     }
#                                 },
#                                 "Louisa",
#                                 {
#                                     "key11": "Hans"
#                                 }
#                             ]
#                         }
#                     },
#                     "Brad"
#                 ]
#             }
#         },
#         "key12": "Kate"
#     }
