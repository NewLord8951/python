a = list(range(20))
print(a)
b = [i for i in a if i > 1 and all(i % j != 0 for j in range(2, i))]
print(b)
