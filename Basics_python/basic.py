import math

x = int(input("Insert first number:"))
y = int(input("Insert second number:"))

add = x + y
substract = x - y
multiply = x * y
divide = x / y

print(add)
#print(substract)
print(multiply)
#print(divide)

th = "there"

"""
print("Hello", "There")
print("Hello" + "there")
"""
print("Hello" + th)
print("Hello", th)


thislist = ["apple", "banana", "peach", "something else"]

for e in thislist:
    print(e)

print("\n" + thislist[2])

ThisIsString = "Oya"
ThisIsAlsoString = 'Haha'
ThisIsInt = 5
ThisIsFloat = 5.4

for i in ThisIsAlsoString:
    print(i)

print("\n\n\n" + "Newlines")



L = "I am Alex"
a = "I am Alex"

if L == a:
    print("Wow they're the same!")
else:
    print("They are different")

if x == y:
    print("both inputs are the same")

u = 0
while u <= 5:
    print("U is now", u)
    u += 1  #same as u = u + 1
o = 5
if o > 1:
    print("O is bigger then 1")
if o < 10:
    print("O is smaller then 10")


def multiply(r, t):
    z = r * t
    return z

print(multiply(x, y))
