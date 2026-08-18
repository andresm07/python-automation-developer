#! --- 2026.08.12 ---

#! BIG O NOTATION EXAMPLES

#! O(1) - CONSTANT
# ? Execution time remains identical regardless of input size
def get_first_element(items: list[int]) -> int:
    if items:
        return items[0]

    return -1


#! O(log n) - LOGARITHMIC
# ? Execution time is cut in half in each step. Typical for algorithms that divide problems recursively or iteratively, ie: Binary Search
def binary_search(sorted_arr: list[int], target: int) -> int:
    low, high = 0, len(sorted_arr) - 1

    while low <= high:
        mid = (low + high) // 2

        if sorted_arr[mid] == target:
            return mid
        elif sorted_arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1


#! O(n) - LINEAR
# ? Execution time grows in direct proportion to input size
def find_max(items: list[int]) -> int:
    if not items:
        return None

    max_value = items[0]

    for item in items[1:]:
        if item > max_value:
            max_value = item

    return max_value


#! O(n log n) - LINEARITHMIC
# ? Common in efficient sorting algorithms. Execution time is split into O (log n) levels and performs O(n) work at each level
def merge_sort(arr: list[int]) -> list[int]:
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    merged = []

    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])

    return merged


#! O(n^2) - QUADRATIC
# ? Performance/Execution is proportional to the square of the input size. Common when working/implementing nested loops
def print_all_pairs(items: list):
    for item1 in items:
        for item2 in items:
            print(item1, item2)


#! O(2^n) - EXPONENTIAL
# ? Execution doubles with every addition to the input dataset.
def fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


#! O(n!) - FACTORIAL
# ? Execution increases at an extreme rate with every element added. Common in brute-force solutions to combinatorial problems, such as generating all permutations or the Traveling Salesperson Problem
def get_permutations(arr: list) -> list[list]:
    if len(arr) == 0:
        return [[]]

    permutations = []

    for i in range(len(arr)):
        current = arr[i]
        remaining = arr[:i] + arr[i + 1 :]

        for p in get_permutations(remaining):
            permutations.append([current] + p)  # noqa: RUF005

    return permutations


#! --- PYTHON GENERATORS ---
# ? Definition: A generator in python is a special type of function that produces a sequence of values on demand (lazily) rather than computing them all at once and storing them in memory. Instead of computing a million items and holding them in RAM, a generator calculates each item only when requested, yielding an O(1) memory footprint regardless of dataset size.

# * YIELD - HOW DOES IT WORK?

# ? Standard functions execute top-to-bottom. When they hit a return statement, they pass back a value and destroy their stack frame (forget all local variables).

#! HOW DOES GENERATOR USE YIELD

# * 1. When called, it does not execute immediately. It returns a generator object.
# * 2. When the user/script/client requests a value using next(generator) or inside a for loop, execution will start or resume
# * 3. Upon hitting yield value, execution will pause, freeze all local states (variables, execution pointers), and passes value back
# * 4. On the next next(generator) call, execution resumes immediately after the yield statement
# * 5. When the function finishes or hits a return, Python raises a StopIteration exception (which for loops catch automatically)


def simple_generator():
    print("Starting generator")
    yield "first"
    print("Resumed after first value")
    yield "second"
    print("Generator finished")


gen = simple_generator()
# print(gen)

# print(next(gen))
# print(next(gen))
# print(next(gen))

#! --- 2026.08.18 ---

import sys
import tracemalloc

#! MEMORY USAGE DETERMINATION

x = [1, 2, 3, 4, 5]
print(f"Memory size: {sys.getsizeof(x)} bytes")


def get_function_memory(func, *args, **kwargs):
    tracemalloc.start()

    result = func(*args, **kwargs)

    #! TUPLE DESTRUCTURING *
    current, peak = tracemalloc.get_traced_memory()

    tracemalloc.stop()

    print(
        f"[{func.__name__}] Net Allocated Memory: {current / (1024 * 1024):.2f} MB"
    )
    print(
        f"[{func.__name__}] Peak Memory Allocation: {peak / (1024 * 1024):.2f} MB"
    )

    return result


def heavy_calculation():
    return [i**2 for i in range(1000000)]


res = get_function_memory(heavy_calculation)

#! TUPLE DESTRUCTURING
# def example():
#     return (1, 2, 3, 4, 5)

# first, second, third, fourth, fifth = example()

#! TIME EXECUTION DETERMINATION

import gc
import time


def get_function_time(func, *args, **kwargs):
    gc.disable()

    start_time = time.perf_counter()

    result = func(*args, **kwargs)

    elapsed_time = time.perf_counter() - start_time

    gc.enable()

    print(f"[{func.__name__}] Execution Time: {elapsed_time:.6f} seconds")

    return result


res = get_function_time(heavy_calculation)
