# Generated by Django 5.2 on 2025-05-20 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='History_Rekomendasi',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('jenjang_pendidikan', models.CharField(max_length=100)),
                ('minat_dan_bakat', models.TextField()),
                ('jalur_pendaftaran_pens', models.CharField(max_length=100)),
                ('rencana_karir', models.CharField(max_length=100)),
                ('rata_rata_nilai_masuk_pens', models.FloatField()),
                ('hasil_rekomendasi', models.CharField(max_length=100)),
                ('tanggal', models.DateField()),
            ],
            options={
                'db_table': 'history_rekomendasi',
            },
        ),
    ]
