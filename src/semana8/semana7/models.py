from django.db import models
from django.utils import timezone

from semana5.models import Cliente


class ClienteInvestigacionQuerySet(models.QuerySet):
	def con_ventas_pendientes(self):
		return self.filter(ventas__estado='pendiente').distinct()

	def del_mes_actual(self):
		hoy = timezone.localdate()
		return self.filter(
			ventas__fecha_venta__year=hoy.year,
			ventas__fecha_venta__month=hoy.month,
		).distinct()


class ClienteReporte(Cliente):
	objects = ClienteInvestigacionQuerySet.as_manager()

	class Meta:
		proxy = True
		verbose_name = 'Cliente para reportes de Semana 7'
		verbose_name_plural = 'Clientes para reportes de Semana 7'
