# Generated by Django 2.1.2 on 2018-10-19 01:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20181019_0145'),
    ]

    operations = [
        migrations.CreateModel(
            name='Verifier_Contract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verified', models.BooleanField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='contract',
            name='verifiers',
        ),
        migrations.AlterField(
            model_name='contract',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.Person'),
        ),
        migrations.AddField(
            model_name='verifier_contract',
            name='contract',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='verify', to='api.Contract'),
        ),
        migrations.AddField(
            model_name='verifier_contract',
            name='verifier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.Person'),
        ),
    ]