from django.db import models

class AnalysisSummary(models.Model):
    id = models.AutoField(primary_key=True)
    analysis_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class Demographics(models.Model):
    id = models.AutoField(primary_key=True)
    analysis_summary = models.ForeignKey(AnalysisSummary, on_delete=models.CASCADE, related_name='demographics')
    type = models.CharField(max_length=255) 
    value = models.TextField()
    count = models.IntegerField()

class TemporalData(models.Model):
    id = models.AutoField(primary_key=True)
    analysis_summary = models.ForeignKey(AnalysisSummary, on_delete=models.CASCADE, related_name='temporal_data')
    year = models.IntegerField()
    count = models.IntegerField()
