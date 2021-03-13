"""
Provide a little bit of abstraction for gis.
"""
from django.db.models import Manager, TextField

try:
    from django.contrib.gis.db.models import MultiPointField, MultiPolygonField
except Exception:
    raise
    def MultiPolygonField(*args, **kw):
        return TextField()
    MultiPointField = MultiPolygonField

GeoManager = Manager
