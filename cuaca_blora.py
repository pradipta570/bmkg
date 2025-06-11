import requests
import json

# Ganti kode wilayah sesuai kebutuhan
kode_wilayah = "33.16.04.2016"
url = f"https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4={kode_wilayah}"

try:
    response = requests.get(url, timeout=10)
    data = response.json()

    # Ambil data cuaca hari ini dan besok
    cuaca_hari_ini = data["data"][0]["cuaca"][0][0]  # Hari ini, jam pertama
    cuaca_besok    = data["data"][0]["cuaca"][1][0]  # Besok, jam pertama

    data_ringkas = {
        "lokasi": data["lokasi"]["kecamatan"],
        "hari_ini": {
            "cuaca": cuaca_hari_ini["weather_desc"],
            "suhu": int(float(cuaca_hari_ini["t"])),
            "kelembapan": int(float(cuaca_hari_ini["hu"]))
        },
        "besok": {
            "cuaca": cuaca_besok["weather_desc"],
            "suhu": int(float(cuaca_besok["t"])),
            "kelembapan": int(float(cuaca_besok["hu"]))
        }
    }

    # Simpan ke file JSON
    with open("cuaca_ringkas.json", "w", encoding="utf-8") as f:
        json.dump(data_ringkas, f, ensure_ascii=False, indent=2)

    print("Berhasil menyimpan cuaca_ringkas.json")

except Exception as e:
    print("Gagal mengambil atau memproses data:", e)
