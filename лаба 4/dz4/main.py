import threading
import random
import time


def partition(arr, low, high):
    """Разделяет массив вокруг опорного элемента."""
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quicksort_sequential(arr, low, high):
    """Последовательная реализация быстрой сортировки."""
    if low < high:
        pivot_index = partition(arr, low, high)
        quicksort_sequential(arr, low, pivot_index - 1)
        quicksort_sequential(arr, pivot_index + 1, high)


def parallel_quicksort(arr, low, high, available_threads, threshold):
    """Параллельная быстрая сортировка с использованием потоков."""
    if high - low + 1 <= threshold:
        arr[low:high + 1] = sorted(arr[low:high + 1])
    else:
        if low < high:
            pivot_index = partition(arr, low, high)
            if available_threads > 1:
                left_threads = available_threads // 2
                right_threads = available_threads - left_threads
                left_thread = threading.Thread(
                    target=parallel_quicksort,
                    args=(arr, low, pivot_index - 1, left_threads, threshold)
                )
                right_thread = threading.Thread(
                    target=parallel_quicksort,
                    args=(arr, pivot_index + 1, high, right_threads, threshold)
                )
                left_thread.start()
                right_thread.start()
                left_thread.join()
                right_thread.join()
            else:
                parallel_quicksort(arr, low, pivot_index - 1, 1, threshold)
                parallel_quicksort(arr, pivot_index + 1, high, 1, threshold)


def quicksort(arr, num_threads, threshold=100):
    """Запускает параллельную сортировку с заданным числом потоков."""
    parallel_quicksort(arr, 0, len(arr) - 1, num_threads, threshold)


if __name__ == "__main__":
    sizes = [100, 1000, 10000, 20000, 30000, 40000, 50000]
    num_threads_list = [2, 4, 8]  # Разное количество потоков
    threshold = 100  # Порог для перехода на стандартную сортировку

    for size in sizes:
        print(f"\nТестирование для размера массива {size}:")
        arr = [random.randint(0, 10000) for _ in range(size)]

        arr_seq = arr.copy()
        start_time = time.perf_counter()
        quicksort_sequential(arr_seq, 0, len(arr_seq) - 1)
        seq_time = time.perf_counter() - start_time
        print(f"Время последовательной сортировки: {seq_time:.6f} секунд")

        for num_threads in num_threads_list:
            arr_par = arr.copy()
            start_time = time.perf_counter()
            quicksort(arr_par, num_threads, threshold)
            par_time = time.perf_counter() - start_time
            speedup = seq_time / par_time if par_time > 0 else 0
            print(f"Параллельная сортировка с {num_threads} потоками: {par_time:.6f} секунд, Ускорение: {speedup:.2f}")
