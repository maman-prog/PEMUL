import tkinter as tk
from tkinter import messagebox
import sqlite3

# Membuat database SQLite
conn = sqlite3.connect("nilai_siswa.db")
cursor = conn.cursor()

# Membuat tabel nilai_siswa
cursor.execute("""
CREATE TABLE IF NOT EXISTS nilai_siswa (
    nama_siswa TEXT,
    biologi REAL,
    fisika REAL,
    inggris REAL,
    prediksi_fakultas TEXT
)
""")

conn.commit()


# Fungsi untuk memproses nilai dan menyimpan data
def submitNilai():
    nama = entry_nama.get().strip()

    try:
        biologi = float(entry_biologi.get())
        fisika = float(entry_fisika.get())
        inggris = float(entry_inggris.get())

        # Validasi nama
        if nama == "":
            messagebox.showwarning(
                "Peringatan",
                "Nama siswa harus diisi!"
            )
            return

        # Validasi nilai
        if not all(0 <= nilai <= 100
                   for nilai in [biologi, fisika, inggris]):
            messagebox.showwarning(
                "Peringatan",
                "Nilai harus berada antara 0 sampai 100!"
            )
            return

        # Menentukan prediksi fakultas
        if biologi > fisika and biologi > inggris:
            prediksi = "Kedokteran"

        elif fisika > biologi and fisika > inggris:
            prediksi = "Teknik"

        elif inggris > biologi and inggris > fisika:
            prediksi = "Bahasa"

        else:
            prediksi = "Tidak ada prediksi tunggal (nilai seri)"

        # Menyimpan data ke database
        cursor.execute("""
        INSERT INTO nilai_siswa
        (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
        """, (nama, biologi, fisika, inggris, prediksi))

        conn.commit()

        # Menampilkan hasil prediksi
        hasil.config(
            text=f"Hasil Prediksi: {prediksi}"
        )

        messagebox.showinfo(
            "Berhasil",
            "Data siswa berhasil disimpan ke database!"
        )

        # Mengosongkan input setelah berhasil
        entry_nama.delete(0, tk.END)
        entry_biologi.delete(0, tk.END)
        entry_fisika.delete(0, tk.END)
        entry_inggris.delete(0, tk.END)

    except ValueError:
        messagebox.showerror(
            "Input Tidak Valid",
            "Masukkan nilai Biologi, Fisika, dan Inggris "
            "dalam bentuk angka!"
        )


# Membuat jendela utama
top = tk.Tk()
top.title("Aplikasi Prediksi Fakultas")
top.geometry("420x450")
top.resizable(False, False)
top.configure(bg="#F0F4F8")


# Label judul
judul = tk.Label(
    top,
    text="Aplikasi Prediksi Fakultas",
    font=("Arial", 16, "bold"),
    bg="#F0F4F8",
    fg="#1E3A5F"
)
judul.pack(pady=20)


 Frame input
frame = tk.Frame(top, bg="#F0F4F8")
frame.pack(pady=10)


# Input nama siswa
tk.Label(
    frame,
    text="Nama Siswa",
    font=("Arial", 11),
    bg="#F0F4F8",
    width=15,
    anchor="w"
).grid(row=0, column=0, padx=10, pady=10)

entry_nama = tk.Entry(frame, width=22)
entry_nama.grid(row=0, column=1, padx=10, pady=10)
# Input nilai Biologi
tk.Label(
    frame,
    text="Nilai Biologi",
    font=("Arial", 11),
    bg="#F0F4F8",
    width=15,
    anchor="w"
).grid(row=1, column=0, padx=10, pady=10)

entry_biologi = tk.Entry(frame, width=22)
entry_biologi.grid(row=1, column=1, padx=10, pady=10)


