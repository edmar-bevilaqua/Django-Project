from django.urls import path
from . import views

urlpatterns = [
    path('', views.clientes, name="clientes"),
    path('atualizar_cliente', views.atualizar_cliente, name="atualizar_cliente"),
    path('atualiza-pet/<int:id>', views.atualiza_pet, name="atualiza_pet"),
    path('add-pet/<int:id>', views.add_pet, name="add_pet"),
    path('deleta-pet/<int:id>', views.deleta_pet, name="deleta_pet"),
    path('atualiza-cliente/<int:id>', views.atualiza_cliente, name="atualiza_cliente")
]
