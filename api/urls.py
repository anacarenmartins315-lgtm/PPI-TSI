from django.urls import path
from api.views import FundoImobiliarioListCreateAPIView, FundoImobiliarioDetailAPIView

urlpatterns = [
    path('fundos/', FundoImobiliarioListCreateAPIView.as_view(), name='fundo-list-create'),
    path('fundos/<uuid:pk>/', FundoImobiliarioDetailAPIView.as_view(), name='fundo-detail'),
]
