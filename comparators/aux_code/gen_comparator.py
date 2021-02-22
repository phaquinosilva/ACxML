
ge = 0
l = 0

for i in range(2**4):
    for j in range(2**4):
        if i < j:
            print(i, j, 1)
            l += 1
        else:
            print(i, j, 0)
            ge += 1

print(l)
print(ge)