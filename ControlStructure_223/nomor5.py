def pola_segitiga(n):
    return [[i] * i for i in range(1, n + 1)]


def main():
    n = int(input("Masukkan nilai n: "))

    for baris in pola_segitiga(n):
        print(*baris)


if __name__ == "__main__":
    main()