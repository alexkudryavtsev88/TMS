''' LESSON 2 '''

l1 = [1, 2, 3]
l2 = [1, 2, 3]

print(id(l1))
print(id(l2))

s1 = {1, 2, 3}
s2 = {1, 2, 3}

print(id(s1))
print(id(s2))


d1 = {1:1, 2:2}
d2 = {1:1, 2:2}

print(id(d1))
print(id(d2))

print()

print(id(list(s1)))
print(id(list(s2)))

print()

print(id(set(l1)))
print(id(set(l2)))

print()

new = [(1, 2), (3, 4), (5, 6)]
print(id(new))
print(id(dict(new)))
print(id(dict(new)))