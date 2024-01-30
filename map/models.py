from django.db import models
from django_admin_geomap import GeoItem


class Contractor(models.Model):
    name = models.CharField(max_length=250)
    marker = models.ImageField(upload_to='markers/')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Контрагент'
        verbose_name_plural = 'Контрагенты'


class Object(models.Model, GeoItem):
    name = models.CharField(max_length=250)
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE)
    address = models.CharField(max_length=1000)
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)

    @property
    def geomap_longitude(self):
        return '' if self.lon is None else str(self.lon)

    @property
    def geomap_latitude(self):
        return '' if self.lat is None else str(self.lat)
    
    @property
    def geomap_popup_edit(self):
        html = f'<b>{self.contractor.name}</b><br/>'
        html += f'<b>{self.name}</b><br/>'
        html += f'<b>Адрес:</b> {self.address}'
        return html
    
    @property
    def geomap_icon(self):
        return self.contractor.marker.url

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'
