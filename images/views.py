from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import ImageAnalysis
from .serializers import ImageAnalysisSerializer, ImageUploadSerializer

# Import with error handling
try:
    from .openai_service import OpenAIImageAnalyzer
    OPENAI_AVAILABLE = True
    print("✅ OpenAI service imported successfully")
except ImportError as e:
    print(f"❌ Failed to import OpenAI service: {e}")
    OPENAI_AVAILABLE = False
except Exception as e:
    print(f"❌ Error initializing OpenAI: {e}")
    OPENAI_AVAILABLE = False


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_image_and_analyze(request):
    """
    Upload an image and return both the image URL + OpenAI analysis result in one response.
    """
    print("📨 Received upload request")
    
    serializer = ImageUploadSerializer(data=request.data)
    
    if serializer.is_valid():
        print("✅ Serializer validation passed")
        
        # Save the image
        image_analysis = serializer.save()
        print(f"💾 Image saved with ID: {image_analysis.id}")
        
        # Handle OpenAI analysis
        analysis_result = "Analysis not available"
        
        if OPENAI_AVAILABLE:
            try:
                print("🤖 Starting OpenAI analysis...")
                analyzer = OpenAIImageAnalyzer()
                analysis_result = analyzer.analyze_image(image_analysis.image.path)
                print(f"📝 Analysis result: {analysis_result[:100]}...")
            except Exception as e:
                analysis_result = f"Analysis service error: {str(e)}"
                print(f"❌ OpenAI analysis failed: {e}")
        else:
            analysis_result = "OpenAI service not available"
            print("⚠️ OpenAI service not available")
        
        image_analysis.analysis_result = analysis_result
        image_analysis.save()
        print("💾 Analysis result saved")
        
        # Return both image URL + analysis result
        response_data = {
            'id': image_analysis.id,
            'image_url': request.build_absolute_uri(image_analysis.image.url),
            'original_filename': image_analysis.original_filename,
            'analysis_result': analysis_result
        }
        print("📤 Sending success response")
        return Response(response_data, status=status.HTTP_201_CREATED)
    else:
        print(f"❌ Serializer errors: {serializer.errors}")
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
