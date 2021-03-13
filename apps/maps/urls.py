#
# Copyright (C) 2017 Maha Farhat
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# pylint: disable=invalid-name
"""
Maps urls
"""

from django.urls import path

from .views import (DrugList, Lineages, LocusList, MapPage, Mutations,
                    MutationView, Places, Sources)

app_name = 'maps'
urlpatterns = [
    path('', MapPage.as_view(), name="map"),
    path('data/sources/', Sources.as_view(), name="map.sources"),
    path('data/places/', Places.as_view(), name="map.places"),
    path('data/drugs/', DrugList.as_view(), name="map.drugs"),
    path('data/lineages/', Lineages.as_view(), name="map.lineages"),
    path('data/locuses/', LocusList.as_view(), name="map.locuses"),
    path('data/mutations/', Mutations.as_view(), name="map.mutations"),
    path('data/mutation/', MutationView.as_view(), name="map.mutation"),
]
