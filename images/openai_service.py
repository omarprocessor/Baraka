import openai
from django.conf import settings
import base64
import os


class OpenAIImageAnalyzer:
    def __init__(self):
        # Check if API key is available
        api_key = settings.OPENAI_API_KEY
        if not api_key:
            raise ValueError("OpenAI API key is missing from settings")
        
        print(f"✅ OpenAI API Key present: {bool(api_key)}")
        
        # Simple initialization for openai==1.3.0
        self.client = openai.OpenAI(api_key=api_key)
    
    def analyze_image(self, image_path):
        """
        Analyze an image using OpenAI's GPT-4 Vision model
        """
        try:
            print(f"🖼️ Starting image analysis for: {image_path}")
            
            # Check if file exists
            if not os.path.exists(image_path):
                return "Error: Image file not found on server"
            
            file_size = os.path.getsize(image_path)
            print(f"📊 Image file size: {file_size} bytes")
            
            # Encode image to base64
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()
                base64_image = base64.b64encode(image_data).decode('utf-8')
            
            print(f"🔤 Base64 encoded image length: {len(base64_image)}")
            
            # Simple prompt
            prompt = "Describe what you see in this image in detail."
            
            print("🚀 Sending request to OpenAI...")
            
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
                max_tokens=500
            )
            
            result = response.choices[0].message.content
            print("✅ OpenAI analysis completed successfully")
            return result
            
        except Exception as e:
            error_msg = f"OpenAI analysis failed: {str(e)}"
            print(f"❌ {error_msg}")
            return error_msg
