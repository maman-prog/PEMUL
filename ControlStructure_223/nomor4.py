def bilangan_ganjil(n):
    return [angka for angka in range(1, n + 1) if angka % 2 != 0]


def main():
    n = int(input("Masukkan nilai n: "))
    print(*bilangan_ganjil(n))


if __name__ == "__main__":
    main()