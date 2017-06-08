# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PeroidTaskRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('excute_param', models.TextField(verbose_name='\u4efb\u52a1\u6267\u884c\u53c2\u6570')),
                ('excute_result', models.TextField(verbose_name='\u4efb\u52a1\u6267\u884c\u7ed3\u679c')),
                ('excute_time', models.DateTimeField(auto_now_add=True, verbose_name='\u4efb\u52a1\u6267\u884c\u65f6\u95f4')),
                ('periodic_task_id', models.IntegerField(default=0, verbose_name='\u5468\u671f\u6027\u4efb\u52a1\u7684id')),
            ],
            options={
                'ordering': ['-excute_time'],
                'verbose_name': '\u5468\u671f\u6027\u4efb\u52a1\u6267\u884c\u8bb0\u5f55',
                'verbose_name_plural': '\u5468\u671f\u6027\u4efb\u52a1\u6267\u884c\u8bb0\u5f55',
            },
        ),
        migrations.CreateModel(
            name='TimingTaskRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=64, verbose_name='\u7528\u6237')),
                ('title', models.TextField(null=True, verbose_name='\u6d88\u606f\u6807\u9898', blank=True)),
                ('content', models.TextField(null=True, verbose_name='\u6d88\u606f\u5185\u5bb9', blank=True)),
                ('create_time', models.DateTimeField(null=True, verbose_name='\u4efb\u52a1\u521b\u5efa\u65f6\u95f4', blank=True)),
                ('excute_time', models.DateTimeField(null=True, verbose_name='\u6267\u884c\u65f6\u95f4', blank=True)),
                ('is_excuted', models.IntegerField(default=0, verbose_name='\u662f\u5426\u6267\u884c')),
            ],
            options={
                'verbose_name': '\u5b9a\u65f6\u4efb\u52a1\u6267\u884c\u8bb0\u5f55',
                'verbose_name_plural': '\u5b9a\u65f6\u4efb\u52a1\u6267\u884c\u8bb0\u5f55',
            },
        ),
    ]
