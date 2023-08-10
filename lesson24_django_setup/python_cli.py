import sys
import os

if __name__ == '__main__':
    list_ = [1, 2, 3, 4, 5]
    args = sys.argv[1:]
    match args:
        case '-la', *_:
            for x in list_:
                print(x)
        case _:
            print(", ".join(str(i) for i in list_))





