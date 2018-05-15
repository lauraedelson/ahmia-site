"""The URL patterns of the ahmia search app."""
from django.conf.urls import url
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    url(r'^i2p/', views.IipResultsView.as_view(), name="results-i2p"), # results
    url(r'^', views.TorResultsView.as_view(), name="results"), # results
    url(r'^redirect', views.OnionRedirectView.as_view(), name="onion_redirect") #redirect to hidden service
]
