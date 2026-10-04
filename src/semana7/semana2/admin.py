from django.contrib import admin

from .models import ObjetoEncontrado, Ubicacion


@admin.register(Ubicacion)
class UbicacionAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


@admin.register(ObjetoEncontrado)
class ObjetoEncontradoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ubicacion', 'fecha', 'contacto')
    search_fields = ('nombre', 'ubicacion__nombre', 'contacto')
    list_filter = ('ubicacion', 'fecha')
