from django.contrib import admin

from .models import Diagnostico, Parcela


class DiagnosticoInline(admin.TabularInline):
    model = Diagnostico
    extra = 0


@admin.register(Parcela)
class ParcelaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cultivo', 'agricultor', 'total_diagnosticos')
    search_fields = ('nombre', 'agricultor', 'referencia')
    inlines = (DiagnosticoInline,)


@admin.register(Diagnostico)
class DiagnosticoAdmin(admin.ModelAdmin):
    list_display = ('plaga_nombre', 'parcela', 'fecha_captura', 'confianza')
    list_filter = ('plaga_detectada', 'fecha_captura')
    search_fields = ('parcela__nombre', 'plaga_nombre', 'plaga_detectada')
