from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import ImageAnalysis
from .serializers import ImageAnalysisSerializer, ImageUploadSerializer
from .openai_service import OpenAIImageAnalyzer


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_image_and_analyze(request):
    """
    Upload an image and return both the image URL + OpenAI analysis result in one response.
    """
    serializer = ImageUploadSerializer(data=request.data)
    
    if serializer.is_valid():
        # Save the image
        image_analysis = serializer.save()
        
        # Run OpenAI analysis synchronously
        analyzer = OpenAIImageAnalyzer()
        analysis_result = analyzer.analyze_image(image_analysis.image.path)
        image_analysis.analysis_result = analysis_result
        image_analysis.save()
        
        # Return both image URL + analysis result
        response_data = {
            'id': image_analysis.id,
            'image_url': request.build_absolute_uri(image_analysis.image.url),
            'original_filename': image_analysis.original_filename,
            'analysis_result': analysis_result
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_analysis_by_name(request, filename):
    """
    Retrieve analysis results by image filename
    """
    image_analysis = get_object_or_404(ImageAnalysis, original_filename=filename)
    serializer = ImageAnalysisSerializer(image_analysis)
    return Response(serializer.data)


@api_view(['GET'])
def get_analysis_by_id(request, image_id):
    """
    Retrieve analysis results by image ID
    """
    image_analysis = get_object_or_404(ImageAnalysis, id=image_id)
    serializer = ImageAnalysisSerializer(image_analysis)
    return Response(serializer.data)


@api_view(['GET'])
def list_all_images(request):
    """
    List all uploaded images and their analysis status
    """
    images = ImageAnalysis.objects.all()
    serializer = ImageAnalysisSerializer(images, many=True)
    return Response(serializer.data)
