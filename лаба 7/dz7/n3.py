def fast_pow(a: int, n: int, mod: int = 10 ** 9 + 7) -> int:
    result = 1
    a %= mod
    while n > 0:
        # если младший бит степени равен 1,то тогда умножаем на текущую основу
        if n & 1:
            result = (result * a) % mod
        # возводим в квадрат
        a = (a * a) % mod
        # сдвигаем биты: делим степень на 2
        n >>= 1
    return result


def main():
    a, n = map(int, input().split())
    print(fast_pow(a, n))


if __name__ == "__main__":
    main()
