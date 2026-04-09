import functools

from utils import measure_time


def fib(n: int) -> int:
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

@functools.cache #Pamatuje si to hodnotu pro každé n - dojede k n = 0 a pak už se jen vynořuje, nevětví se cestou nazpátek
def fib_cache(n: int) -> int:
    if n <= 1:
        return n
    return fib_cache(n - 1) + fib_cache(n - 2)

def fib_mem(n: int, lookup: dict[int, int]) -> int: #Identocké co fib_cache, ale jiná práce s pamětí
    if n <= 1:
        return n

    if n not in lookup:
        lookup[n] = fib_mem(n - 1,lookup) + fib_mem(n - 2,lookup)

    return lookup[n]

def fib_iter(n: int) -> int:
    if n <= 1:
        return n
    
    f: list[int] = [0] * (n+1)
    f[1] = 1

    for i in range(2, n + 1):
        f[i] = f[i - 1] + f[i - 2]
    return f[n]


def main() -> None:
    lookup: dict[int, int] = {}

    a = 20 # to je hned
    #a = 30 # to už chvilku trvá
    #a = 40 # za jak dlouho se asi dočkáme?
    print("Klasicky:")
    measure_time(lambda: fib(a))
    print(f"Číslo: {a}")
    print("Cache:")
    measure_time(lambda: fib_cache(a))
    print("fib_mem:")
    measure_time(lambda: fib_mem(a, lookup))
    print("Nejrychlejsi:")
    measure_time(lambda: fib_iter(a))

    print(fib_cache(a))
    print(fib_iter(a))


if __name__ == "__main__":
    main()
