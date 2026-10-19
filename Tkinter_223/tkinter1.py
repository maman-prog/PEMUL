import tkinter as tk

top = tk.Tk()
top.title("Aplikasi Prediksi Prodi Pilihan")
top.geometry("450x600")
top.resizable(False, False)

# Label judul
judul = tk.Label(
    top,
    text="Aplikasi Prediksi Prodi Pilihan",
    font=("Arial", 16, "bold")
)
judul.pack(pady=15)

# Frame untuk input nilai
frame = tk.Frame(top)
frame.pack(pady=5)

# 10 input nilai mata pelajaran

mata_pelajaran = [
    "Pendidikan Agama",
    "PPKn",
    "Bahasa Indonesia",
    "Matematika",
    "Bahasa Inggris",
    "Seni Budaya",
    "PJOK",
    "Prakarya",
    "Bahasa Daerah",
    "Informatika"
]


entries = []

for i, pelajaran in enumerate(mata_pelajaran):
    label = tk.Label(frame, text=pelajaran, width=18, anchor="w")
    label.grid(row=i, column=0, padx=10, pady=5)

    entry = tk.Entry(frame, width=20)
    entry.grid(row=i, column=1, padx=10, pady=5)

    entries.append(entry)

# Fungsi hasil prediksi
def hasilPrediksi():
    hasil.config(text="Hasil Prediksi: Teknologi Informasi")

# Tombol hasil prediksi
tombol = tk.Button(
    top,
    text="Hasil Prediksi",
    command=hasilPrediksi,
    font=("Arial", 11, "bold")
)
tombol.pack(pady=15)

# Label luaran hasil prediksi
hasil = tk.Label(
    top,
    text="Hasil Prediksi: -",
    font=("Arial", 12, "bold"),
    fg="blue"
)
hasil.pack(pady=5)

top.mainloop()
