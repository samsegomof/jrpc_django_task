from django.urls import path
from .views import JsonRpcFormView

urlpatterns = [
    path('', JsonRpcFormView.as_view(), name='rpc_view'),
]
