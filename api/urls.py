from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
#Clase usada para documentar con la herramineta swagger
from rest_framework_swagger.views import get_swagger_view
#Clase usada para documentar con la herramienta corapi
from rest_framework.documentation import include_docs_urls

#Instanciamineto de la clase get_swagger_view
schema_view = get_swagger_view(title='RestFul Api Curso DRF')


router = DefaultRouter()
router.register('v2/productos', views.ProductoViewSet, basename='productos')

urlpatterns = [
    path('v1/productos/', views.ProductoList.as_view(), name='producto_list'),
    path('v1/productos/<int:pk>', views.ProductoDetalle.as_view(), name='producto_detalle'),
    path('v1/categorias/', views.CategoriaList.as_view(), name='categoria_save'),
    path('v1/subcategorias/', views.SubCategoriaListAll.as_view(), name='subcategoira_save'),
    path('v1/categorias/<int:pk>', views.CategoriaDetalle.as_view(), name='categoria_detalle'),
    path('v1/categorias/<int:pk>/subcategorias/', views.SubCategoriaList.as_view(), name='sc_list'),
    path('v1/categorias/<int:cat_pk>/addsubcategorias/', views.SubCategoriaAdd.as_view(), name='sc_add'),
    path('v3/usuarios/', views.UserCreate.as_view(), name='usuarios'),
    path('v4/login/', views.LoginView.as_view(), name='login'),
    path('v4/login-drf/', obtain_auth_token, name='login_drf'),
    #Path para ejecutar la herramienta de swagger
    path('swagger-docs/', schema_view),
    #Path para ejecutar la herramienta de coreapi
    path('coreapi-docs', include_docs_urls(title='Documentacion COREAPI')),
]

urlpatterns += router.urls