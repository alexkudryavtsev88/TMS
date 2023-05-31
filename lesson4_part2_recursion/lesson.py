from collections import deque

x = [1, 2, 3, 4, 5]
dq = deque(x)
print(dq)

dq.append(6)  # Добавление элемента в КОНЕЦ за Константное время
print(dq)
dq.pop()      # Удаление элемента с КОНЦА за Константное время
print(dq)
dq.appendleft(10)  # Добавление элемента в НАЧАЛО за Константное время
print(dq)
dq.popleft()   # Удаление элемента из НАЧАЛА за Константное время
print(dq)