from django.shortcuts import render
from django.http import JsonResponse
from .models import Matkul, InfoProdi, UserForML

# Create your views here.
def home_page(request):
    return render(request,"home.html")

def about_page(request):
    return render(request,"about.html")

def input_page(request):
    return render(request,"input.html")

def result_page(request):
    return render(request,"result.html")

def prodi_page(request):
    return render(request,'kuota_prodi.html')

def snbp_page(request):
    return render(request,'kuota_snbp.html')

def snbt_page(request):
    return render(request,'kuota_snbt.html')

def mandiri_page(request):
    return render(request,'kuota_mandiri.html')