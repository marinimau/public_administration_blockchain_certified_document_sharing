# Generated by Django 3.2.5 on 2021-07-21 15:27

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=60)),
                ('description', models.TextField(max_length=500, null=True)),
                ('require_permission', models.BooleanField(default=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='user.paoperator')),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('citizen', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='user.citizen')),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='document.document')),
            ],
            options={
                'unique_together': {('citizen', 'document')},
            },
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('citizen', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='user.citizen')),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='document.document')),
            ],
            options={
                'unique_together': {('citizen', 'document')},
            },
        ),
        migrations.CreateModel(
            name='DocumentVersion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('creation_timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('file_resource', models.FileField(upload_to='')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='user.paoperator')),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='document.document')),
            ],
            options={
                'unique_together': {('creation_timestamp', 'document')},
            },
        ),
    ]
