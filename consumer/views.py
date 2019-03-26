# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from fotocasa import settings

from django.shortcuts import render, redirect
from django.http.response import HttpResponse, HttpResponseNotFound


def photos(request, place, filename):
    path = os.path.join(settings.BASE_DIR, 'photos/{place}/{filename}'.format(place=place, filename=filename))
    try:
        with open(path, 'rb') as f:
            return HttpResponse(f.read(), content_type='image/jpeg')
    except IOError as e:
        print e.message
        return HttpResponseNotFound()


def property_view(request, slug, property_id):
    """
    """
    return render(request, 'property/property.html', {'slug': slug, 'id': property_id})


def property_contact(request):
    data = request.POST.copy()

    return redirect('property_view', property_id=12, slug='aaaa')
