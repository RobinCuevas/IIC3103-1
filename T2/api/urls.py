from django.urls import path
from .views import HamburguesaViewSet,HamburguesaDetails, IngredienteViewSet, IngredienteDetails, HamburguesaIngrediente

urlpatterns = [
    path('hamburguesa/', HamburguesaViewSet.as_view()),
    path('hamburguesa/<int:id>', HamburguesaDetails.as_view()),
    path('ingrediente/', IngredienteViewSet.as_view()),
    path('ingrediente/<int:id>', IngredienteDetails.as_view()),
    path('hamburguesa/<int:id>/ingrediente/<int:ide>', HamburguesaIngrediente.as_view()),
]