import openai
from django.conf import settings
import base64
import os


class OpenAIImageAnalyzer:
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
    
    def analyze_image(self, image_path):
        """
        Analyze an image using OpenAI's GPT-4 Vision model
        """
        try:
            # Encode image to base64
            with open(image_path, "rb") as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            
            # Create the analysis prompt
            prompt = """
            Analyze this image and provide a detailed description. Include:
            1. What objects, people, or scenes are visible
            2. Colors, lighting, and composition
            3. Any text that appears in the image
            4. The overall mood or atmosphere
            5. Any interesting or notable details
            
            Please provide a comprehensive analysis in a clear, structured format.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error analyzing image: {str(e)}"
