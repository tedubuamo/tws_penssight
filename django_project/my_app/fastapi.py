from fastapi import FastAPI, Query
from pydantic import BaseModel
from asgiref.sync import sync_to_async # type: ignore
from collections import defaultdict
from typing import Optional
from datetime import date
import pandas as pd
import joblib

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")
django.setup()
from .models import InfoProdi, Matkul, History_Rekomendasi

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "model.pkl")
metadata_path = os.path.join(BASE_DIR, "metadata.pkl")

# Skema input
class InputData(BaseModel):
    Jenjang_Pendidikan: str
    Minat_dan_Bakat: list[str]
    Jalur_Pendaftaran_PENS: str
    Rencana_Karir: str
    Rata_rata_Nilai_Masuk_PENS: float

rekomendasi_cache = {}

@app.post("/rekomendasi_prodi")
async def rekomendasi(data_user: InputData):
    try:
        model = joblib.load(model_path)
        metadata = joblib.load(metadata_path)

        minat_bakat_columns = metadata['minat_bakat_columns']
        X_columns = metadata['X_columns']
        reverse_mapping = metadata['reverse_mapping']

        # Buat DataFrame dari input
        data_df = pd.DataFrame([{
            'Jalur Pendaftaran PENS': data_user.Jalur_Pendaftaran_PENS,
            'Jenjang Pendidikan': data_user.Jenjang_Pendidikan,
            'Minat dan Bakat': data_user.Minat_dan_Bakat,
            'Rata-rata Nilai Masuk PENS': data_user.Rata_rata_Nilai_Masuk_PENS,
            'Rencana Karir': data_user.Rencana_Karir
        }])

        # Proses 'Minat dan Bakat'
        minat_bakat_dummies = data_df['Minat dan Bakat'].str.get_dummies(sep=', ')
        for col in minat_bakat_columns:
            if col not in minat_bakat_dummies.columns:
                minat_bakat_dummies[col] = 0
        minat_bakat_dummies = minat_bakat_dummies[minat_bakat_columns]

        # Gabung dan urutkan kolom
        data_baru_processed = data_df.drop('Minat dan Bakat', axis=1)
        data_baru_final = pd.concat([data_baru_processed, minat_bakat_dummies], axis=1)
        data_baru_final = data_baru_final[X_columns]

        # Prediksi
        prediksi = model.predict(data_baru_final)[0]
        hasil = reverse_mapping[prediksi]

        # Simpan ke dictionary sementara
        rekomendasi_cache["hasil"] = hasil

        await sync_to_async(History_Rekomendasi.objects.create)(
            jenjang_pendidikan=data_user.Jenjang_Pendidikan,
            minat_dan_bakat=', '.join(data_user.Minat_dan_Bakat),
            jalur_pendaftaran_pens=data_user.Jalur_Pendaftaran_PENS,
            rencana_karir=data_user.Rencana_Karir,
            rata_rata_nilai_masuk_pens=data_user.Rata_rata_Nilai_Masuk_PENS,
            hasil_rekomendasi=hasil,
            tanggal=date.today() 
        )

        return {"Program Studi": hasil}

    except Exception as e:
        print("Terjadi error:", str(e))
        return {"error": str(e)}

@app.get("/hasil_rekomendasi")
async def hasil():
    hasil_prodi = rekomendasi_cache.get("hasil")
    prodi = await sync_to_async(InfoProdi.objects.get)(prodi=hasil_prodi)
    matkul = await sync_to_async(Matkul.objects.get)(id=prodi.id_prodi)

    # Define each variable
    nama_prodi = prodi.prodi
    deskripsi_singkat = prodi.deskripsi_singkat
    matkul_smt1_d3 = matkul.matkul_smt1_d3
    matkul_smt2_d3 = matkul.matkul_smt2_d3
    matkul_smt3_d3 = matkul.matkul_smt3_d3
    matkul_smt4_d3 = matkul.matkul_smt4_d3
    matkul_smt5_d3 = matkul.matkul_smt5_d3
    matkul_smt6_d3 = matkul.matkul_smt6_d3
    matkul_smt1_d4 = matkul.matkul_smt1_d4
    matkul_smt2_d4 = matkul.matkul_smt2_d4
    matkul_smt3_d4 = matkul.matkul_smt3_d4
    matkul_smt4_d4 = matkul.matkul_smt4_d4
    matkul_smt5_d4 = matkul.matkul_smt5_d4
    matkul_smt6_d4 = matkul.matkul_smt6_d4
    matkul_smt7_d4 = matkul.matkul_smt7_d4
    matkul_smt8_d4 = matkul.matkul_smt8_d4
    prospek_kerja = matkul.prospek_kerja
    link_website = matkul.link_website

    return {
        "prodi": nama_prodi,
        "deskripsi_singkat" : deskripsi_singkat,
        "matkul_smt1_d3" : matkul_smt1_d3,
        "matkul_smt2_d3" : matkul_smt2_d3,
        "matkul_smt3_d3" : matkul_smt3_d3,
        "matkul_smt4_d3" : matkul_smt4_d3,
        "matkul_smt5_d3" : matkul_smt5_d3,
        "matkul_smt6_d3" : matkul_smt6_d3,
        "matkul_smt1_d4" : matkul_smt1_d4,
        "matkul_smt2_d4" : matkul_smt2_d4,
        "matkul_smt3_d4" : matkul_smt3_d4,
        "matkul_smt4_d4" : matkul_smt4_d4,
        "matkul_smt5_d4" : matkul_smt5_d4,
        "matkul_smt6_d4" : matkul_smt6_d4,
        "matkul_smt7_d4" : matkul_smt7_d4,
        "matkul_smt8_d4" : matkul_smt8_d4,
        "prospek_kerja" : prospek_kerja,
        "link_website" : link_website,
    }

@app.get("/grafik_rekomendasi")
async def grafik(day: Optional[str] = Query(None), month: Optional[str] = Query(None), year: Optional[str] = Query(None)):
    queryset = await sync_to_async(list)(History_Rekomendasi.objects.values())

    # Filter berdasarkan tanggal jika diberikan
    if day and month and year:
        try:
            filter_date = f"{year.zfill(4)}-{month.zfill(2)}-{day.zfill(2)}"
            queryset = [item for item in queryset if item['tanggal'].strftime('%Y-%m-%d') == filter_date]
        except Exception as e:
            return {"error": f"Format tanggal tidak valid: {e}"}

    # Buat struktur {"2025-05-19": {"Sains Data Terapan": 2}, ...}
    result = defaultdict(lambda: defaultdict(int))
    for item in queryset:
        tanggal_str = item['tanggal'].strftime('%Y-%m-%d')  # Ubah objek tanggal ke string
        rekomendasi = item['hasil_rekomendasi']
        result[tanggal_str][rekomendasi] += 1

    # Konversi nested defaultdict ke dict biasa agar bisa diubah jadi JSON
    final_result = {tanggal: dict(rekom) for tanggal, rekom in result.items()}

    return final_result