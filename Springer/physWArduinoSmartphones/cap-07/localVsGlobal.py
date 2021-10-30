a = 3

def fun1():
    b = 2 * a
    return b

def fun2(a):
    a *= 2
    return a

def fun3(b):
    a = 7
    return a

print('{} {}'.format(a, fun1()))
print('{} {}'.format(a, fun2(a)))
print('{} {}'.format(a, fun3(a)))
print(a)
