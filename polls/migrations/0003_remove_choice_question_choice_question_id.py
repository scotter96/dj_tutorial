# Generated by Django 4.1.3 on 2022-11-02 16:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_alter_choice_question'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='question',
        ),
        migrations.AddField(
            model_name='choice',
            name='question_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='choice_ids', related_query_name='choice_id', to='polls.question'),
            preserve_default=False,
        ),
    ]