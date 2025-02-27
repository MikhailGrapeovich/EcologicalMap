"""l = [1, 2, 3]


class ReversedList(list):
    def __iter__(self):
        for i in reversed(self):
            print("до yield")

            yield i
            print("после yield")


for e in l:
    print(e)

l = ReversedList()
l.append(1)
l.append(2)
l.append(3)

for i in l:
    print(i)
"""
"""
import asyncio
import time

async def func1(x):
    print(x**2)
    await asyncio.sleep(3)
    print(f"{func1.__name__} завершена")
async def func2(x):
    print(x**0.5)
    await asyncio.sleep(3)
    print(f"{func2.__name__} завершена")

async def summ(n: int, r: int = 2):
    summa = 0
    for i in range(r):
        print(time.strftime("%X"))
        summa += await asyncio.create_task(sumint(n//r*i, n//r+n//r*i))
        print(time.strftime("%X"))
    return summa

async def sumint(f, t):
    summa = 0
    for i in range(f,t):
        summa +=i
    return summa

async def main():
    task = asyncio.create_task(summ(500001,2))
#    task2 = asyncio.create_task(func2(1))
    return await task
#    await task2
if __name__ == "__main__":
    print(asyncio.run(main()))
n = 500000
print((n*(n+1))/2)

"сумма от 1 до 500000"


class Foo:
    n=5
f = Foo()
setattr(f,"n", 10)
print(getattr(f, "n"))
"""

from sqlalchemy import select
from app.models.user import User

print(select(User).where(getattr(User, "username") == "qwerty"))