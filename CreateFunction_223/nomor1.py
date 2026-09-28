def Converts_temperature(value, unit):
    if unit == "C":
        return value * 9/5 + 32
    elif unit == "F":
        return (value - 32) * 5/9
    else:
        return None


Input_value = float(input("Masukkan value: "))
Input_unit = input("Masukkan unit (C/F): ").strip().upper()

Konversi = Converts_temperature(Input_value, Input_unit)

if Input_unit == "C":
    print(f"Hasil konversi: {Konversi:.2f} °F")
elif Input_unit == "F":
    print(f"Hasil konversi: {Konversi:.2f} °C")
else:
    print("Unit tidak valid. Masukkan C atau F.")