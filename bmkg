import requests
import xml.etree.ElementTree as ET
import json

URL = "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-Blora.xml"

def ambil_data_bmkg():
    response = requests.get(URL)
    response.raise_for_status()
    return response.content

def parse_bmkg(xml_data):
    root = ET.fromstring(xml_data)
    hasil = {}

    for area in root.findall(".//area"):
        nama = area.get("description").lower().replace(" ", "_")
        suhu_min, suhu_max, hum_min, hum_max, cuaca = None, None, None, None, None

        for param in area.findall("parameter"):
            id_param = param.get("id")

            if id_param == "t":  # suhu
                values = param.findall("timerange/value")
                if len(values) >= 2:
                    suhu_min = int(values[0].text)
                    suhu_max = int(values[1].text)
            elif id_param == "hu":  # kelembapan
                values = param.findall("timerange/value")
                if len(values) >= 2:
                    hum_min = int(values[0].text)
                    hum_max = int(values[1].text)
            elif id_param == "weather":  # cuaca
                cuaca_code = param.find("timerange/value").text
                kode_dict = {
                    "0": "Cerah", "1": "Cerah Berawan", "2": "Cerah Berawan", "3": "Berawan",
                    "4": "Berawan Tebal", "5": "Udara Kabur", "10": "Asap", "45": "Kabut",
                    "60": "Hujan Ringan", "61": "Hujan Sedang", "63": "Hujan Lebat",
                    "95": "Hujan Petir", "97": "Hujan Petir"
                }
                cuaca = kode_dict.get(cuaca_code, "Tidak Diketahui")

        hasil[nama] = {
            "cuaca": cuaca,
            "suhu_min": suhu_min,
            "suhu_max": suhu_max,
            "kelembapan_min": hum_min,
            "kelembapan_max": hum_max
        }

    return hasil

def simpan_json(data):
    with open("cuaca_blora.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    xml = ambil_data_bmkg()
    data_json = parse_bmkg(xml)
    simpan_json(data_json)
    print("✅ cuaca_blora.json berhasil dibuat.")
