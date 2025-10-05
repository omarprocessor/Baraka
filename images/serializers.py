from rest_framework import serializers
from .models import ImageAnalysis


class ImageAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageAnalysis
        fields = ['id', 'image', 'original_filename', 'analysis_result', 'created_at', 'updated_at']
        read_only_fields = ['id', 'analysis_result', 'created_at', 'updated_at']


class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageAnalysis
        fields = ['image']
    
    def create(self, validated_data):
        # Get the original filename from the uploaded file
        image_file = validated_data['image']
        validated_data['original_filename'] = image_file.name
        return super().create(validated_data)
