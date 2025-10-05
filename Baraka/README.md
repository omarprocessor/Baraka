# Django Image Analyzer API

A Django REST API that allows uploading images and automatically analyzes them using OpenAI's GPT-4 Vision model.

## Features

- Upload images via REST API
- Automatic image analysis using OpenAI GPT-4 Vision
- Retrieve analysis results by image name or ID
- List all uploaded images
- Admin interface for managing images
- CORS support for frontend integration

## Setup

### 1. Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the project root:

```bash
cp env_example.txt .env
```

Edit the `.env` file and add your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Database Setup

```bash
# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

### 4. Run the Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## API Endpoints

### Upload Image
- **POST** `/api/upload/`
- **Content-Type**: `multipart/form-data`
- **Body**: `image` (file)
- **Response**: Image details with unique ID

### Get Analysis by Filename
- **GET** `/api/analysis/{filename}/`
- **Response**: Complete analysis data

### Get Analysis by ID
- **GET** `/api/analysis/id/{image_id}/`
- **Response**: Complete analysis data

### List All Images
- **GET** `/api/list/`
- **Response**: List of all uploaded images

## Usage Examples

### Upload an Image

```bash
curl -X POST \
  http://localhost:8000/api/upload/ \
  -H 'Content-Type: multipart/form-data' \
  -F 'image=@/path/to/your/image.jpg'
```

### Get Analysis by Filename

```bash
curl http://localhost:8000/api/analysis/image.jpg/
```

### Get Analysis by ID

```bash
curl http://localhost:8000/api/analysis/id/123e4567-e89b-12d3-a456-426614174000/
```

## Response Format

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "image": "/media/images/uuid.jpg",
  "original_filename": "image.jpg",
  "analysis_result": "Detailed analysis of the image...",
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

## Admin Interface

Access the Django admin at `http://localhost:8000/admin/` to:
- View all uploaded images
- Check analysis status
- Manage image records

## Project Structure

```
image_analyzer/
├── images/
│   ├── models.py          # ImageAnalysis model
│   ├── serializers.py     # API serializers
│   ├── views.py           # API views
│   ├── urls.py            # URL patterns
│   ├── admin.py           # Admin configuration
│   └── openai_service.py  # OpenAI integration
├── image_analyzer/
│   ├── settings.py        # Django settings
│   └── urls.py            # Main URL configuration
├── media/                 # Uploaded images storage
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Notes

- Images are automatically analyzed in the background after upload
- Analysis results are stored in the database
- The API supports CORS for frontend integration
- Images are stored with UUID filenames to prevent conflicts
- OpenAI API key is required for image analysis functionality

## Requirements

- Python 3.8+
- Django 4.2.7
- OpenAI API key
- Valid image files (JPEG, PNG, etc.)
