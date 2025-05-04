from django.urls import path
from .views import home_page, about_page, input_page, result_page, prodi_page, snbp_page, snbt_page, mandiri_page

urlpatterns = [
    path('', home_page, name='home_page'),
    path('about_page/', about_page, name='about_page'),
    path('input_page/', input_page, name='input_page'),
    path('result_page/', result_page, name='result_page'),
    path('kuota_prodi/', prodi_page, name='prodi_page'),
    path('kuota_snbt/', snbt_page, name='snbt_page'),
    path('kuota_snbp/', snbp_page, name='snbp_page'),
    path('kuota_mandiri/', mandiri_page, name='mandiri_page'),
]