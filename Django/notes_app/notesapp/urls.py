
from django.urls import path
from . import views

urlpatterns =[
    path("notes/" , views.notes , name="notes"),
    path("notes_detail/<slug:slugGiven>/", views.notes_detail , name="notes_detail")
]