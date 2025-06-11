import requests
import json

# Kode wilayah Kedungtuban (dengan titik)
ADM4_KEDUNGTUBAN = "33.16.04.2016"
API_URL = f"https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4={ADM4_KEDUNGTUBAN}"

def ambil_data():
    resp = requests.get(API_URL, timeout=10)
    resp.raise_for_status()
    return resp.json()

def sederhanakan(data):
    lokasi = data.get("lokasi", {})
    prakiraan = data.get("data", [])
    
    hasil = {
        "lokasi": {
            "desa": lokasi.get("desa"),
            "kecamatan": lokasi.get("kecamatan"),
            "kotkab": lokasi.get("kotkab"),
            "provinsi": lokasi.get("provinsi")
        },
        "prakiraan": []
    }

    for hari_ke, blok in enumerate(prakiraan[:2]):  # Hari ini dan besok
        for item in blok.get("cuaca", []):
            hasil["prakiraan"].append({
                "hari": hari_ke + 1,
                "jam": item.get("local_datetime"),
                "cuaca": item.get("weather_desc"),
                "suhu": item.get("t"),
                "kelembapan": item.get("hu")
            })

    return hasil

def simpan_json(data, nama_file="cuaca_kedungtuban.json"):
    with open(nama_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ Data disimpan di {nama_file}")

if __name__ == "__main__":
    try:
        data = ambil_data()
        ringkas = sederhanakan(data)
        simpan_json(ringkas)
    except Exception as e:
        print("❌ Gagal:", e)
