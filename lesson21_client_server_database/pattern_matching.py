def get_value(key: int) -> tuple[str, ...] | None:
    my_dict: dict[int, tuple[str, ...]] = {
        1: ("test", ),
        2: ("Alex", "Ann"),
        3: ("0", "1", "2", "3", "4"),
        4: (),
    }
    return my_dict.get(key)


def match_result(result):
    match result:
        case None:
            print("value not found!")
        case name_1, name_2:
            print(f"Two names: {name_1}, {name_2}")
        case "0", *_:
            print([int(n) for n in result])
        case _, "1" | "2", *_:
            print([int(n) for n in result])
        case _:
            print("I don't know what to do!")


for i in range(5):
    result = get_value(i)
    match_result(result)