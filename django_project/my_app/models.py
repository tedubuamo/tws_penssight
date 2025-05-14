from django.db import models

# Create your models here.
class InfoProdi(models.Model):
    id_prodi = models.AutoField(primary_key=True)
    prodi = models.CharField(max_length=255)
    deskripsi_singkat = models.TextField()

    class Meta:
        managed = False
        db_table = 'infoprodi'


class Matkul(models.Model):
    id = models.BigAutoField(primary_key=True)
    matkul_smt1_d3 = models.TextField(blank=True, null=True)
    matkul_smt2_d3 = models.TextField(blank=True, null=True)
    matkul_smt3_d3 = models.TextField(blank=True, null=True)
    matkul_smt4_d3 = models.TextField(blank=True, null=True)
    matkul_smt5_d3 = models.TextField(blank=True, null=True)
    matkul_smt6_d3 = models.TextField(blank=True, null=True)
    matkul_smt1_d4 = models.TextField(blank=True, null=True)
    matkul_smt2_d4 = models.TextField(blank=True, null=True)
    matkul_smt3_d4 = models.TextField(blank=True, null=True)
    matkul_smt4_d4 = models.TextField(blank=True, null=True)
    matkul_smt5_d4 = models.TextField(blank=True, null=True)
    matkul_smt6_d4 = models.TextField(blank=True, null=True)
    matkul_smt7_d4 = models.TextField(blank=True, null=True)
    matkul_smt8_d4 = models.TextField(blank=True, null=True)
    id_prodi = models.OneToOneField(InfoProdi, models.DO_NOTHING)
    prospek_kerja = models.TextField(blank=True, null=True)
    link_website = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'matkul'


class UserForML(models.Model):
    jenjang_pendidikan = models.CharField(max_length=50)
    minat_bakat = models.TextField()
    jalur_pendaftaran = models.TextField()
    rata_nilai = models.DecimalField(max_digits=65535, decimal_places=65535)
    rencana_karir = models.TextField()
    prodi_rekomendasi = models.ForeignKey(InfoProdi, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'userforml'