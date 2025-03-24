from django.urls import path
from .views import download_csv_tier_report, download_excel_tier_report

urlpatterns = [
    path('generate-report/csv/<str:tier_code>/', download_csv_tier_report, name='download_csv_tier_report'),
    path('generate-report/excel/', download_excel_tier_report, name='download_excel_tier_report'),
]
