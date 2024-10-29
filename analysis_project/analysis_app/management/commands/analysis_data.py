from django.core.management.base import BaseCommand
from analysis_app.models import AnalysisSummary, Demographics, TemporalData
import pandas as pd
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Analyze data and store in database'

    def handle(self, *args, **kwargs):
        # Load data
        file_path = os.path.join(settings.BASE_DIR, 'static/data/data.xlsx')
        df = pd.read_excel(file_path, sheet_name='Sheet1')
        
        # Create a new analysis summary
        analysis_summary = AnalysisSummary.objects.create(analysis_name="Data Analysis")

        # 1. Data Completeness Analysis
        missing_data = df.isnull().mean() * 100
        for column, missing_percentage in missing_data.items():
            Demographics.objects.create(analysis_summary=analysis_summary, type="Data Completeness", value=column, count=missing_percentage)

        # 2. Citizenship and Birthplace Distribution
        for citizenship, count in df['Citizenship'].value_counts().items():
            Demographics.objects.create(analysis_summary=analysis_summary, type="Citizenship", value=citizenship, count=count)
        
        for birthplace, count in df['Place of Birth'].value_counts().items():
            Demographics.objects.create(analysis_summary=analysis_summary, type="Birthplace", value=birthplace, count=count)

        # 3. Temporal Distribution Analysis
        df['Control Date'] = pd.to_datetime(df['Control Date'], errors='coerce')
        for year, count in df['Control Date'].dt.year.value_counts().items():
            TemporalData.objects.create(analysis_summary=analysis_summary, year=year, count=count)

        self.stdout.write(self.style.SUCCESS("Data analysis complete and saved to the database."))
