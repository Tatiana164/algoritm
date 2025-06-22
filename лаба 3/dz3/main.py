import unittest
import random
import time


def merge_sort(arr):
    if len(arr) <= 1:
        return arr[:]
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def counting_sort_for_radix(arr, exp):
    buckets = [[] for _ in range(10)]
    for num in arr:
        digit = (num // exp) % 10
        buckets[digit].append(num)
    return [num for bucket in buckets for num in bucket]


def radix_sort(arr):
    if not arr:
        return []
    result = arr[:]
    max_num = max(result)
    exp = 1
    while max_num // exp > 0:
        result = counting_sort_for_radix(result, exp)
        exp *= 10
    return result


def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quick_sort_recursive(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        quick_sort_recursive(arr, low, pi - 1)
        quick_sort_recursive(arr, pi + 1, high)


def quick_sort(arr):
    result = arr[:]
    if result:
        quick_sort_recursive(result, 0, len(result) - 1)
    return result


def get_array(length):
    array = list(range(1, length + 1))
    random.shuffle(array)
    return array


def benchmark_sorts():
    array_lengths = [1000, 10000, 25000, 40000, 50000]
    for n in array_lengths:
        print(f"\n📦 Массив из {n} элементов:")

        arr = get_array(n)
        start = time.perf_counter()
        merge_sort(arr)
        end = time.perf_counter()
        print(f"🔷 Merge Sort: {round((end - start) * 1000, 2)} мс")

        arr = get_array(n)
        start = time.perf_counter()
        radix_sort(arr)
        end = time.perf_counter()
        print(f"🔶 Radix Sort: {round((end - start) * 1000, 2)} мс")

        arr = get_array(n)
        start = time.perf_counter()
        quick_sort(arr)
        end = time.perf_counter()
        print(f"🔺 Quick Sort: {round((end - start) * 1000, 2)} мс")


def demonstrate_examples():
    print("\n📌 Демонстрация алгоритмов на небольшом массиве:\n")
    input_data = [42, 17, 8, 99, 5, 66, 23]
    input_data_2 = [4, 5, 8, 7, 5]

    print("🔷 Merge Sort:")
    result = merge_sort(input_data)
    result2 = merge_sort(input_data_2)
    print(f"Вход: {input_data}")
    print(f"Выход: {result}")
    print(f"Вход: {input_data_2}")
    print(f"Выход: {result2}\n")

    print("🔶 Radix Sort:")
    result = radix_sort(input_data)
    result2 = radix_sort(input_data_2)
    print(f"Вход: {input_data}")
    print(f"Выход: {result}")
    print(f"Вход: {input_data_2}")
    print(f"Выход: {result2}\n")

    print("🔺 Quick Sort:")
    result = quick_sort(input_data)
    result2 = radix_sort(input_data_2)
    print(f"Вход: {input_data}")
    print(f"Выход: {result}")
    print(f"Вход: {input_data_2}")
    print(f"Выход: {result2}\n")


class TestSortingAlgorithms(unittest.TestCase):
    def test_merge_sort(self):
        self.assertEqual(merge_sort([5, 2, 9, 1, 5, 6]), [1, 2, 5, 5, 6, 9])

    def test_radix_sort(self):
        self.assertEqual(radix_sort([170, 45, 75, 90, 802, 24, 2, 66]), [2, 24, 45, 66, 75, 90, 170, 802])

    def test_quick_sort(self):
        self.assertEqual(quick_sort([3, 2, 1]), [1, 2, 3])


if __name__ == '__main__':
    unittest.main(exit=False)
    benchmark_sorts()
    demonstrate_examples()
