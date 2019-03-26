# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.admin.filters import RelatedFieldListFilter
from .property import Tag, Photo, Property
from .location import Country, Region, Province, City, District


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('property', 'name', 'display_photo', )
    list_filter = ('property__name', )


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'property_type', 'location_name', )
    list_filter = ('property_type', 'district__name')


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    pass


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', )


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'province', 'country', )


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'province', 'country', )


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'region', 'province', 'country',)
