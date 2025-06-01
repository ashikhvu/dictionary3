# n = []
# for i in range(6):
#     n.append(i)
# print(n)

# n= [i for i in range(6)]
# print(n)

# n=[]
# for i in range(6):
#     n.append(i*2)
# print(n)

# n = [ i*2 for i in range(6)]
# print(n)

# n = [i for i in range(10) if i%2 == 0]
# print(n)

# word = ["hello","welcome"]
# n = [i.upper() for i in word]
# print(n)

# def add(x,y):
#     return x+y
# print(add(10,4))

# add = lambda x,y:x+y
# print(add(50,55))

# print((lambda x,y:x+y)(55,11))
import random
print(''.join([str(random.randint(1,9)) for _ in range(6)]))
