from collections import deque
import queue

x = [1, 2, 3, 4, 5]
dq = deque(x)
print(dq)

dq.append(6)
print(dq)
dq.pop()
print(dq)
dq.appendleft(10)
print(dq)
dq.popleft()
print(dq)