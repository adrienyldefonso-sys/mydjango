import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('semana2', '0002_ubicacion_alter_objetoencontrado_ubicacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='objetoencontrado',
            name='ubicacion',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='objetos',
                to='semana2.ubicacion',
            ),
        ),
    ]
