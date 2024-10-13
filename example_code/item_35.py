#!/usr/bin/env PYTHONHASHSEED=1234 python3

# Copyright 2014-2019 Brett Slatkin, Pearson Education Inc.
# Licensed under the Apache License, Version 2.0 (the "License");

# 军规35: Avoid Causing State Transitions in Generators with throw
# 生成器中避免使用 throw 引发状态转换

"""
整体总结:
不要使用 throw() 在生成器中引发状态转换，因为它增加了代码的复杂性和维护难度。
推荐做法：将状态管理和异常处理逻辑放在生成器外部，或者使用状态机实现复杂状态转换。

特定场景总结：何时使用这种模式？
适用场景：当生成器需要处理复杂的状态管理，如可重置计时器、重试逻辑等。
避免滥用：如果生成器逻辑简单，尽量不要使用 throw() 进行状态转换，以免增加不必要的复杂性。
比如范例：在计时器生成器中，使用 throw() 实现重置计时器的功能。 timer() 生成器在收到 Reset 异常时，重置计数器。
"""

import random

random.seed(1234)
import logging
from pprint import pprint
from sys import stdout as STDOUT
import atexit
import gc
import io
import os
import tempfile

TEST_DIR = tempfile.TemporaryDirectory()
atexit.register(TEST_DIR.cleanup)

OLD_CWD = os.getcwd()
atexit.register(lambda: os.chdir(OLD_CWD))
os.chdir(TEST_DIR.name)


def close_open_files():
    everything = gc.get_objects()
    for obj in everything:
        if isinstance(obj, io.IOBase):
            obj.close()


atexit.register(close_open_files)

# Example 1
# 目的：演示生成器如何处理异常。
# 解释：创建一个生成器，使用 it.throw() 引发自定义异常。
# 结果：捕获并记录 MyError 异常。
print(f"\n{'Example 1':*^50}")
try:
    class MyError(Exception):
        pass


    def my_generator():
        yield 1
        yield 2
        yield 3


    it = my_generator()
    print(next(it))  # Yield 1
    print(next(it))  # Yield 2
    print(it.throw(MyError('test error')))
except:
    logging.exception('Expected')
else:
    assert False

# Example 2
# 目的：展示生成器中的异常处理。
# 解释：在生成器中使用 try 捕获 MyError。
# 结果：打印 "Got MyError!"，然后继续生成其他值。
print(f"\n{'Example 2':*^50}")


def my_generator():
    yield 1
    try:
        yield 2
    except MyError:
        print('Got MyError!')
    else:
        yield 3
    yield 4


it = my_generator()
print(next(it))  # Yield 1
print(next(it))  # Yield 2
print(it.throw(MyError('test error')))

# Example 3
# 目的：使用生成器和自定义异常来重置状态。
# 解释：定义 timer 生成器，可以在 Reset 异常被捕获时重置计数器。
# 结果：生成器在收到 Reset 异常时，计数器重置为初始值。
print(f"\n{'Example 3':*^50}")


class Reset(Exception):
    pass


def timer(period):
    current = period
    while current:
        current -= 1
        try:
            yield current
        except Reset:
            current = period


# Example 4
# 目的：结合外部事件和生成器控制。
# 解释：通过轮询外部事件决定继续计时还是重置计时器。
# 结果：在外部事件发生时，生成器根据需要重置计时。
print(f"\n{'Example 4':*^50}")
RESETS = [
    False, False, False, True, False, True, False,
    False, False, False, False, False, False, False]


def check_for_reset():
    return RESETS.pop(0)


def announce(remaining):
    print(f'{remaining} ticks remaining')


def run():
    it = timer(4)
    while True:
        try:
            if check_for_reset():
                current = it.throw(Reset())
            else:
                current = next(it)
        except StopIteration:
            break
        else:
            announce(current)


run()

# Example 5
# 目的：使用类实现计时器功能。
# 解释：Timer 类包含重置功能，并通过迭代器接口提供计时。
# 结果：通过迭代 Timer 类，输出每个计时值。
print(f"\n{'Example 5':*^50}")


class Timer:
    def __init__(self, period):
        self.current = period
        self.period = period

    def reset(self):
        self.current = self.period

    def __iter__(self):
        while self.current:
            self.current -= 1
            yield self.current


# Example 6
# 目的：整合类和外部事件处理。
# 解释：使用 Timer 类，在计时过程中根据外部事件决定是否重置计时器。
# 结果：在每次迭代中，根据外部事件决定是否重置计时器。
print(f"\n{'Example 6':*^50}")
RESETS = [
    False, False, True, False, True, False,
    False, False, False, False, False, False, False]

def run():
    timer = Timer(4)
    for current in timer:
        if check_for_reset():
            timer.reset()
        announce(current)

run()
