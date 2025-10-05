from django.contrib import admin
from .models import ImageAnalysis


@admin.register(ImageAnalysis)
class ImageAnalysisAdmin(admin.ModelAdmin):
    list_display = ['original_filename', 'created_at', 'has_analysis']
    list_filter = ['created_at']
    search_fields = ['original_filename']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    def has_analysis(self, obj):
        return bool(obj.analysis_result)
    has_analysis.boolean = True
    has_analysis.short_description = 'Has Analysis'