from django.contrib import admin
from django.urls import path
from receipt.views.receipt_views import upload_receipt, receipt_list, edit_receipt, export_csv
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', receipt_list, name='receipt_list'),
    path('upload/', upload_receipt, name='upload_receipt'),
    path('edit/<int:pk>/', edit_receipt, name='edit_receipt'),
    path('export/', export_csv, name='export_csv'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)