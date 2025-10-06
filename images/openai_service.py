import requests
import json
import base64
import os
from django.conf import settings


class OpenAIImageAnalyzer:
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        if not self.api_key:
            raise ValueError("OpenAI API key is missing from settings")
        print(f"✅ OpenAI API Key present: {bool(self.api_key)}")
    
    def analyze_image(self, image_path):
        """
        Analyze an image using OpenAI's GPT-4 Vision model via direct API call
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
            
            # Prepare the API request
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            payload = {
                "model": "gpt-4-vision-preview",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Describe what you see in this image in detail. Include objects, colors, composition, and any notable details."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 500
            }
            
            print("🚀 Sending request to OpenAI API...")
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=60  # Increased timeout for image analysis
            )
            
            print(f"📡 OpenAI API response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()['choices'][0]['message']['content']
                print("✅ OpenAI analysis completed successfully")
                return result
            else:
                error_data = response.json() if response.content else {}
                error_msg = f"OpenAI API error {response.status_code}: {error_data}"
                print(f"❌ {error_msg}")
                return error_msg
            
        except requests.exceptions.Timeout:
            error_msg = "OpenAI API request timed out"
            print(f"❌ {error_msg}")
            return error_msg
        except Exception as e:
            error_msg = f"OpenAI analysis failed: {str(e)}"
            print(f"❌ {error_msg}")
            return error_msg
