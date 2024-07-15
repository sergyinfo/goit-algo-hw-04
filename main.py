"""
This script measures the execution time of the merge sort and insertion sort algorithms.
"""
import timeit
import random
import pandas as pd

def merge_sort(arr: list) -> None:
    """
    Sorts the given array using the merge sort algorithm.

    :param arr: The array to be sorted.

    :return: None
    """
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0

        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

def insertion_sort(arr: list) -> None:
    """
    Sorts the given array using the insertion sort algorithm.

    :param arr: The array to be sorted.

    :return: None
    """
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def measure_time(sort_func: callable, data: list, use_sorted: bool=False) -> float:
    """
    Measures the execution time of the given sorting function.

    :param sort_func: The sorting function to be measured.
    :param data: The data to be sorted.
    :param use_sorted: Whether to use the built-in sorted function.

    :return: The execution time of the sorting function.
    """
    if use_sorted:
        setup_code = ""
        stmt = f"sorted({data})"
    else:
        setup_code = f"from __main__ import {sort_func.__name__}"
        stmt = f"{sort_func.__name__}({data})"
    times = timeit.repeat(stmt, setup=setup_code, repeat=5, number=1)
    return min(times)

# Генеруємо тестові дані
data_sizes = [100, 1000, 10000, 100000]
test_data = {size: [random.randint(0, 100000) for _ in range(size)] for size in data_sizes}

# Вимірювання часу виконання
results = {}
for size, data in test_data.items():
    results[size] = {
        'merge_sort': measure_time(merge_sort, data.copy()),
        'insertion_sort': measure_time(insertion_sort, data.copy() if size <= 1000 else data[:1000]),  # обмежимо сортування вставками для великих масивів
        'timsort': measure_time(sorted, data.copy(), True)
    }

df_results = pd.DataFrame(results).T
print(df_results)
