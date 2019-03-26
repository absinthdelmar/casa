# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from uuid import uuid4

from django.utils.translation import gettext as _
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from fotocasa.settings import BASE_DIR
from .location import District


PROPERTY_TYPE_APARTMENT = 0
PROPERTY_TYPE_HOUSE = 1
PROPERTY_TYPE_GARAGE = 2
PROPERTY_TYPE_OFFICE = 3
PROPERTY_TYPE_LAND = 4
PROPERTY_TYPE_ROOM = 5
PROPERTY_TYPE_BUILDING = 6

PROPERTY_TYPES = (
    (PROPERTY_TYPE_APARTMENT, _('Apartment')),
    (PROPERTY_TYPE_HOUSE, _('House')),
    (PROPERTY_TYPE_GARAGE, _('Garage')),
    (PROPERTY_TYPE_OFFICE, _('Office')),
    (PROPERTY_TYPE_LAND, _('Land')),
    (PROPERTY_TYPE_ROOM, _('Room')),
    (PROPERTY_TYPE_BUILDING, _('Building')),
)


class Tag(models.Model):
    name = models.CharField('Name', max_length=64)

    def __unicode__(self):
        return self.name


class Property(models.Model):
    class Meta:
        verbose_name_plural = 'Properties'

    name = models.CharField('Name', max_length=255)
    slug = models.SlugField('Slug', help_text='Short name')
    description = models.TextField('Description')
    district = models.ForeignKey(District)
    property_type = models.IntegerField('Type', default=PROPERTY_TYPE_APARTMENT, choices=PROPERTY_TYPES)
    tags = models.ManyToManyField(Tag, related_name='tags', related_query_name='tag')

    @property
    def location_name(self):
        return '%s' % (self.district.full_name, )

    def __unicode__(self):
        return self.name


def photo_upload_filename(instance, filename):
    ext = filename.split('.')[-1]
    return 'photos/{property}/{name}.{ext}'.format(
        property=instance.property.id, name=uuid4().get_hex(), ext=ext
    )


@receiver(pre_delete)
def on_delete(sender, instance, **kwargs):
    if sender == Photo:
        try:
            url = instance.content.url.split('/')[-1]
            os.remove(os.path.join(BASE_DIR, 'photos', str(instance.property.id), url))
        except Exception as e:
            print e


class Photo(models.Model):
    content = models.ImageField('Image file', upload_to=photo_upload_filename, default='')
    name = models.CharField('Name', max_length=255, default='')
    property = models.ForeignKey(Property, related_name='properties', related_query_name='property')

    def display_photo(self):
        return '<a href="/consumer/{url}" target="_blank">' \
               '<img class="photo" src="/consumer/{url}" height="50" alt="{name}" title="{name}">' \
               '</a>'.format(url=self.content.url, name=self.name)

    display_photo.allow_tags = True

    def __unicode__(self):
        return self.content.name
