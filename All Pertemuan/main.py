import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk


def create_db():
    conn = sqlite3.connect("kesehatan_mental_mahasiswa.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS data_mahasiswa (
            nim INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            semester INTEGER NOT NULL,
            jam_tidur REAL NOT NULL,
            tingkat_stres INTEGER NOT NULL,
            status_kecemasan TEXT NOT NULL,
            hasil_prediksi TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def prediksi_kesehatan_mental(tingkat_stres):
    if tingkat_stres >= 8:
        return "Risiko Lebih Tinggi", "#ff5555"  # Merah
    elif 5 <= tingkat_stres <= 7:
        return "Risiko Sedang", "#ffb86c"  # Kuning
    else:
        return "Risiko Rendah", "#50fa7b"  # Hijau


def submit_data():
    nama = entry_nama.get().strip()
    nim = entry_nim.get().strip()
    status_kecemasan = combo_kecemasan.get()

    if not nama or not nim:
        messagebox.showerror(
            "Error Validasi", "Nama dan NIM mahasiswa tidak boleh kosong!"
        )
        return

    try:
        semester = int(entry_semester.get())
        jam_tidur = float(entry_jam_tidur.get())
        tingkat_stres = int(entry_stres.get())
    except ValueError:
        messagebox.showerror(
            "Error Validasi",
            "Semester, Jam Tidur, dan Tingkat Stres harus berupa angka yang valid!",
        )
        return

    if not (1 <= tingkat_stres <= 10):
        messagebox.showerror(
            "Error Validasi", "Tingkat Stres harus berupa bilangan bulat antara 1 sampai 10!"
        )
        return

    if not (1 <= jam_tidur <= 24):
        messagebox.showerror(
            "Error Validasi", "Jam Tidur harus berupa angka antara 1 sampai 24!"
        )
        return

    if not status_kecemasan:
        messagebox.showerror(
            "Error Validasi", "Status Kecemasan wajib dipilih!"
        )
        return

    hasil, warna = prediksi_kesehatan_mental(tingkat_stres)

    conn = sqlite3.connect("kesehatan_mental_mahasiswa.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO data_mahasiswa (nama, nim, semester, jam_tidur, tingkat_stres, status_kecemasan, hasil_prediksi)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (nama, nim, semester, jam_tidur, tingkat_stres, status_kecemasan, hasil),
    )
    conn.commit()
    conn.close()

    lbl_card_result.config(text=hasil, fg=warna)
    messagebox.showinfo("Sukses", "Data kesehatan mental berhasil dianalisis dan disimpan!")

   
    entry_nama.delete(0, tk.END)
    entry_nim.delete(0, tk.END)
    entry_semester.delete(0, tk.END)
    entry_jam_tidur.delete(0, tk.END)
    entry_stres.delete(0, tk.END)
    combo_kecemasan.set("")
