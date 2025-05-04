from fastapi import FastAPI

app = FastAPI()

@app.get("/api/heloo")
def read_root():
    return {"message":"Hello From Fast API"}

#     path('api/list_matkul/<int:id_prodi_id>', views.list_matkul, name='list_matkul'),
#     path('api/info_prodi/<int:id_prodi>', views.prodi, name='info_prodi'),

# def list_matkul(request, id_prodi_id):
#     list_matkul = Matkul.objects.filter(id_prodi_id=id_prodi_id).values()
#     return JsonResponse(list(list_matkul), safe=False)

# def prodi(request, id_prodi):
#     list_prodi = InfoProdi.objects.filter(id_prodi=id_prodi).values()
#     return JsonResponse(list(list_prodi), safe=False)