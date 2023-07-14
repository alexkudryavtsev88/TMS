"""
Async programming theory
"""
import asyncio

"""
ASYNCHRONOUS PROGRAMMING (Async) is the approach
to execute the I/O tasks concurrently
without the cases when one task blocks another one

In Python It's some alternative to the Threading approach,
but this approach has both pluses and minuses

Pluses:
- When we use Async instead of Threading we don't have
an Overhead to spawning and scheduling of 'executable units':
- in Async, the 'executable unit' names Task, this is a Python object.
- Mechanism for running, scheduling and generally managing the Coroutines
names the Event Loop, and this is also a Python object 
(the another one implementation of the Event Loop written in C exist, but default Event Loop written in Python).
Therefore, the spawning of the Tasks is cheaper than spawning of the Threads and
switching between the Tasks is faster than between the Threads, because we don't need to:
- send signals to OS Kernel when spawning/switching Threads
- Task object doesn't need additional resources for the spawning

Minuses:
- to write the Async code we need to use special async/await syntax, which was added to the 
Python language not so far
- When we write the Async code we need to use special functions - Coroutines, 
which similar to the Python's generators. The difference in that we need to use 
Coroutines almost EVERYWHERE, and any Async code should be run using the 'asyncio.run()' 

What are Coroutines?

1. The Coroutine, in simple words, is a Python function which definition starts not with 'def' but with 'async def'
"""


async def coro():
    print('Hello!')
    return 0

"""
2. The function marked as 'async' is defined as Coroutine upon initialization by the Python Interpreter.
This function can contain any Python code (not only some Async code), but, anyway, if the function's definitions starts with 
 'async' word - be sure that this is Coroutine.
3. If you call the Coroutine function in standard way like this: 
"""

x = coro()

"""
You will get 'coroutine object' in your 'x'
Code inside the Coroutine function is not started executing yet.
(This behavior is so similar to the Generator functions!)
And also you will see the following in your console: "RuntimeWarning: coroutine 'coro' was never awaited"
This is not an Error, just a Warning which reminds us that we need to use special 'await' operator 
when we run the Coroutine

4. To start the execution of the Coroutine you need to call the Async function with 'await' operator
like in commented line bellow:
"""

# result = await coro()

"""
But here we have a problem with this code as above, because we CANNOT to use 'await' operator
outside the another Async function! Therefore we cannot call Coroutines through 'await' in our code
on the MODULE level. 
To run the Coroutine we need to place its call with 'await' to the some another Coroutine
and then run it through the asyncio.run()
"""


async def main():
    result = await coro()
    print(f"Result from Coroutine '{coro.__qualname__}' is {result}")
    return result

asyncio.run(main())


