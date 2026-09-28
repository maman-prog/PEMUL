def deret_fibonacci(batas):
    hasil = []
    a, b = 0, 1
    while a <= batas:
        hasil.append(a)
        a, b = b, a + b
    return hasil


def main():
    n = int(input("Masukkan batas nilai n: "))
    print(*deret_fibonacci(n))


if __name__ == "__main__":
    main()