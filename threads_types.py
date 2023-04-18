"""
A demo showing run_in_executor for different type of executors. I think this demo
is kinda confusing since I don't really grasp the difference between them.

Printout:
    Main thread 139935256930112

    1. Default thread pool starts
    In thread 139935239182080
    1. Default thread pool result:
       b'\x9c\xefF0\xa4\x85u-\xf5d9\xe4\x02\xc7\xbe{\x1b\xc1!\x0b\xd4w\x8a\x96Lx\xa0J:\x0f\xb2:\xba%\xc0\xe9\x82\xf6\x00\x98\xc7\t\xbe,NT\x10=[-r\xa2\x021\xf0D\xd6Q\x92\x9dw\x88\xaf\x8c\xbd\xb3\xed\x0c2\xf8`\xf3\xa2\x12\x19\xa2Uv\xf9\xd2\x7fz\x07\xd3\xcan\x07\xba\xe6\xd7Rp\r\x86\x82\x86\x8fp.\t'

    Fast executor 1

    2. Custom thread pool starts
    In thread 139935230789376
    2. Custom thread pool result:
       b'\xdfl\xcb\x00l\xcf:\x0eXy\xbb\xe2\xd5C\xb4\x1fo\xc6\xfbb\xc2\x05>\x8c\xc9\xc4L\xc7\xbarG@F\xfb^\x95fa6\nn<\xa9\x91\xc7\xecd\xc5\x92\x85Q\xd6\x10\x15A\x0c\xa4\xb0\xa7r\xf3n\xcd\x0b\xa7\xbfdx#\xfb\x8f\xe6\xd4\xca\x9b\xeb\xdc\x8d\x16\x00wP\xd1\xd6\xec\x88\x04\xce\xf2\x0c\x12\xdd\xbe\x03\xbd\xceT\x93\x1c)'

    Fast executor 2

    3. Custom process pool starts
    In thread 139935256930112
    3. Custom process pool result:
       333333283333335000000

    Fast executor 3
"""

import asyncio
import concurrent.futures
import time
import threading

def blocking_io():
    print(f"In thread {threading.get_ident()}")
    time.sleep(2)
    # File operations (such as logging) can block the
    # event loop: run them in a thread pool.
    with open('/dev/urandom', 'rb') as f:
        return f.read(100)

def cpu_bound():
    # CPU-bound operations will block the event loop:
    # in general it is preferable to run them in a
    # process pool.
    print(f"In thread {threading.get_ident()}")
    return sum(i * i for i in range(10 ** 7))

async def fast_executor(i):
    print(f"\nFast executor {i}")

async def test(loop):
    # 1. Run in the default loop's executor. Asyncio will wait with next execution until this returns
    # for some reason. blocking_io will be executed in a new thread.
    print('\n1. Default thread pool starts')
    result = await loop.run_in_executor(None, blocking_io)
    print('1. Default thread pool result:\n', result)

async def main():
    print(f"Main thread {threading.get_ident()}")
    loop = asyncio.get_event_loop()

    # Below will wait until test returns
    await test(loop)

    # Below three lines would run task1 and task2 in parallell and do:
        # 1. Default thread pool starts
        # Fast executor x
        # 1. Default thread pool result
        # Fast executor 1
        # ...
    # task1 = asyncio.create_task(test(loop))
    # task2 = asyncio.create_task(fast_executor("x"))
    # await task1

    # Below line would make it run in the following order:
        # Fast executor 1
        # 2. Custom thread pool starts
        # 1. Default thread pool starts
        # Fast executor x
        # 2. Custom thread pool result
        # Fast executor 2
        # 3. Custom process pool starts
        # 1. Default thread pool result
        # 3. Custom process pool result
        # Fast executor 3
    #asyncio.gather(test(loop), fast_executor("x"))

    await fast_executor(1)

    # 2. Run in a custom thread pool. blocking_io will be executed in a new thread.
    # This is a blocking call.
    with concurrent.futures.ThreadPoolExecutor() as pool:
        print('\n2. Custom thread pool starts')
        result = await loop.run_in_executor(pool, blocking_io)
        print('2. Custom thread pool result:\n', result)

    await fast_executor(2)

    # 3. Run in a custom process pool. blocking_io will be executed in the main thread.
    # This is a blocking call.
    with concurrent.futures.ProcessPoolExecutor() as pool:
        print('\n3. Custom process pool starts')
        result = await loop.run_in_executor(pool, cpu_bound)
        print('3. Custom process pool result:\n', result)

    await fast_executor(3)

if __name__ == '__main__':
    asyncio.run(main())