from django.contrib import admin
from django_admin_geomap import ModelAdmin
from .models import Object, Contractor
from geopy.geocoders import Nominatim
from PIL import Image
from django.db.models import Q


@admin.register(Contractor)
class ContractorAdmin(admin.ModelAdmin):
    list_display = ('name', 'marker')
    list_filter = ('name',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.marker:
            max_size = (40, 40)
            image_path = obj.marker.path
            image = Image.open(image_path)
            image.thumbnail(max_size)
            image.save(image_path)


@admin.register(Object)
class MapObject(ModelAdmin):
    list_display = ('name', 'contractor', 'address', 'lat', 'lon',)
    list_filter = ('name', 'contractor', 'address',)
    search_fields = ('address',)
    geomap_field_latitude = "id_lat"
    geomap_field_longitude = "id_lon"
    geomap_autozoom = "4"

    def save_model(self, request, obj, form, change):
        geocoder = Nominatim(user_agent="geomap_admin")
        location = geocoder.geocode(obj.address)
        if location:
            obj.lat = location.latitude
            obj.lon = location.longitude
        super().save_model(request, obj, form, change)

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if search_term:
            search_word_1 = Q(address__icontains=search_term.lower())
            search_word_2 = Q(address__icontains=search_term.upper())
            search_word_3 = Q(address__icontains=search_term[0].upper() + search_term[1:].lower())
            queryset |= self.model.objects.filter(search_word_1 | search_word_2 | search_word_3)

        return queryset, use_distinct