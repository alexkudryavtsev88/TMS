
def match_result(dict_: dict[int, tuple[str, ...]], key: int) -> str:
    result = dict_.get(key)
    match result:
        case None:
            return "Case 1 (None): value not found!"
        case name_1, name_2:
            return f"Case 2 (Two names): {name_1}, {name_2}"
        case "0", *_:
            return f"Case 3 (Numbers started from 0): {[int(n) for n in result]}"
        case _, "1" | "2", *_:
            return f"Case 4 (Numbers, second number is 1 OR 2): {[int(n) for n in result]}"
        case element, :
            return f"Case 5 (Tuple with only one element): {element}"
        case _:
            return "Case Unknown: I don't know that to do!"


my_dict = {
    1: ("test", ),
    2: ("Alex", "Ann"),
    3: ("0", "1", "2", "3", "4"),
    4: ("-1", "1", "2", "3", "4"),
    5: (),
}
for i in range(6):
    result = match_result(my_dict, i)
    print(f"key: {i}, result: {result}")
