def angka_terbesar(a, b, c):
    if a >= b and a >= c:
        return a
    if b >= c:
        return b
    return c


def main():
    a = float(input("Masukkan angka pertama: "))
    b = float(input("Masukkan angka kedua: "))
    c = float(input("Masukkan angka ketiga: "))

    print("Angka terbesar:", angka_terbesar(a, b, c))


if __name__ == "__main__":
    main()