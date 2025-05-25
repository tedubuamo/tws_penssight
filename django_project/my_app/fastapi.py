from fastapi import FastAPI, Query, status
from fastapi.responses import JSONResponse
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
import logging

# Inisialisasi logger
app = FastAPI()

logging.basicConfig(level=logging.INFO)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "model.pkl")
metadata_path = os.path.join(BASE_DIR, "metadata.pkl")

# Skema input
class InputData(BaseModel):
    jenjang_pendidikan: str
    minat_bakat: list[str]
    jalur_pendaftaran: str
    rata_nilai: float
    rencana_karir: str

rekomendasi_cache = {}

@app.post("/rekomendasi_prodi")
async def rekomendasi(data_user: InputData):
    try:
        # Load model dan metadata
        model = joblib.load(model_path)
        metadata = joblib.load(metadata_path)

        minat_bakat_columns = metadata['minat_bakat_columns']
        X_columns = metadata['X_columns']

        # Buat DataFrame dari input
        data_df = pd.DataFrame([{
            'jalur_pendaftaran': data_user.jalur_pendaftaran,
            'jenjang_pendidikan': data_user.jenjang_pendidikan,
            'minat_bakat': ', '.join(data_user.minat_bakat or []),
            'rata_nilai': data_user.rata_nilai,
            'rencana_karir': data_user.rencana_karir,
        }])

        # Proses minat dan bakat (one-hot encoding)
        minat_bakat_dummies = data_df['minat_bakat'].str.get_dummies(sep=', ')
        for col in minat_bakat_columns:
            if col not in minat_bakat_dummies.columns:
                minat_bakat_dummies[col] = 0
        minat_bakat_dummies = minat_bakat_dummies[minat_bakat_columns]

        # Gabung dan sesuaikan urutan kolom
        data_baru_processed = data_df.drop('minat_bakat', axis=1)
        data_baru_final = pd.concat([data_baru_processed, minat_bakat_dummies], axis=1)
        data_baru_final = data_baru_final.reindex(columns=X_columns, fill_value=0)

        # Prediksi
        hasil_prediksi = model.predict(data_baru_final)[0]
        logging.info(f"Hasil prediksi model: {hasil_prediksi}")

        # Cache jika dibutuhkan
        rekomendasi_cache["hasil"], rekomendasi_cache["prodi"] = hasil_prediksi, data_user.jenjang_pendidikan
        logging.info(f"hasil_rekomendasi:{rekomendasi_cache}")
        # Simpan ke database
        await sync_to_async(History_Rekomendasi.objects.create)(
            jenjang_pendidikan=data_user.jenjang_pendidikan,
            minat_dan_bakat=', '.join(data_user.minat_bakat or []),
            jalur_pendaftaran=data_user.jalur_pendaftaran,
            rencana_karir=data_user.rencana_karir,
            rata_rata_nilai_masuk_pens=data_user.rata_nilai,
            hasil_rekomendasi=hasil_prediksi,
            tanggal=date.today()
        )

        return {"Program Studi": hasil_prediksi, "Jenjang Pendidikan": data_user.jenjang_pendidikan}

    except Exception as e:
        logging.error(f"Terjadi error saat prediksi program studi: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(e)}
        )


@app.get("/hasil_rekomendasi")
async def hasil():
    hasil_prodi = rekomendasi_cache.get("hasil")
    hasil_jenjang = rekomendasi_cache.get("prodi")
    prodi = await sync_to_async(InfoProdi.objects.get)(prodi__iexact=hasil_prodi)
    logging.info(f"Hasil Prodi: {prodi}")
    matkul = await sync_to_async(Matkul.objects.get)(id_prodi=prodi.id_prodi)

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

    if hasil_jenjang == "D3":
        return {
            "prodi": nama_prodi,
            "deskripsi_singkat" : deskripsi_singkat,
            "matkul_smt1_d3" : matkul_smt1_d3,
            "matkul_smt2_d3" : matkul_smt2_d3,
            "matkul_smt3_d3" : matkul_smt3_d3,
            "matkul_smt4_d3" : matkul_smt4_d3,
            "matkul_smt5_d3" : matkul_smt5_d3,
            "matkul_smt6_d3" : matkul_smt6_d3,
            "prospek_kerja" : prospek_kerja,
            "link_website" : link_website,
        }
    
    if hasil_jenjang == "D4":
        return {
            "prodi": nama_prodi,
            "deskripsi_singkat" : deskripsi_singkat,
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
async def grafik():
    queryset = await sync_to_async(list)(History_Rekomendasi.objects.values())

    # Hitung jumlah masing-masing hasil rekomendasi
    result = defaultdict(int)
    for item in queryset:
        hasil = item['hasil_rekomendasi']
        result[hasil] += 1

    return dict(result)