# Generated by Django 4.1.5 on 2023-01-20 13:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('wireguard', '0003_alter_dns_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='allowedip',
            name='ip_address_node',
            field=models.PositiveSmallIntegerField(blank=True, null=True,
                                                   verbose_name='IP узел'),
        ),
    ]
