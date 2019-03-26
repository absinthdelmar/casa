from django.conf.urls import url
from views import property_view, property_contact, photos

consumer_urls = [
    url(r'photos/(?P<place>[0-9]+)/(?P<filename>.+)$', photos, name='photos'),
    url(r'property/(?P<slug>[a-zA-Z0-9_]+)/(?P<property_id>[0-9]+)', property_view, name='property_view'),
    url(r'contact/', property_contact, name='property_contact'),
]
