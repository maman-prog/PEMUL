class PersegiPanjang:
    # Konstruktor untuk mengisi properti panjang dan lebar
    def __init__(self, panjang, lebar):
        self.panjang = panjang
        self.lebar = lebar

    # Menghitung keliling
    def keliling(self):
        return 2 * (self.panjang + self.lebar)

    # Menghitung luas
    def luas(self):
        return self.panjang * self.lebar

    # Menampilkan objek dalam bentuk string
    def __str__(self):
        return (
            f"persegi panjang, panjang {self.panjang} cm, "
            f"dan lebar {self.lebar} cm"
        )


# Membuat objek
persegi = PersegiPanjang(3, 2)

# Menampilkan objek, keliling, dan luas
print(persegi)
print(f"Keliling: {persegi.keliling()} cm")
print(f"Luas: {persegi.luas()} cm²")