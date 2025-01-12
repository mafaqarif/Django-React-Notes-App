
from django.urls import path
from . import views

urlpatterns =[
    path("notes/" , views.notes , name="notes"),
    path("notes/<slug:slugGiven>/", views.notes_detail , name="note-details")
]