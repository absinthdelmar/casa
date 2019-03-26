# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Location hierarchy concept
# Country -> Province -> Region -> City -> District
#
# Examples:
#
# Spain -> Barcelona -> Barcelones -> Barcelona Capital -> Gracia
# Poland -> Lesser Poland -> Krakow Area -> Krakow -> Podgorze
# Ukraine -> Odessa -> Odessa -> Odessa -> Primorski

class Country(models.Model):
    class Meta:
        verbose_name_plural = 'Countries'
    name = models.CharField('Name', max_length=255)

    def __unicode__(self):
        return self.name


class Province(models.Model):
    country = models.ForeignKey(Country)
    name = models.CharField('Name', max_length=255)

    def __unicode__(self):
        return self.name


class Region(models.Model):
    province = models.ForeignKey(Province)
    name = models.CharField('Name', max_length=255)

    @property
    def country(self):
        return self.province.country

    def __unicode__(self):
        return self.name


class City(models.Model):
    class Meta:
        verbose_name_plural = 'Cities'
    region = models.ForeignKey(Region)
    name = models.CharField('Name', max_length=255)

    @property
    def country(self):
        return self.region.province.country

    @property
    def province(self):
        return self.region.province

    @property
    def full_name(self):
        return '%s %s %s %s' % (self.name, self.region, self.province, self.country)

    def __unicode__(self):
        return self.name


class District(models.Model):
    city = models.ForeignKey(City)
    name = models.CharField('Name', max_length=255)

    @property
    def country(self):
        return self.city.region.province.country

    @property
    def province(self):
        return self.city.region.province

    @property
    def region(self):
        return self.city.region

    @property
    def full_name(self):
        return '%s, %s, %s, %s, %s' % (self.name, self.city, self.region, self.province, self.country)

    def __unicode__(self):
        return self.name
