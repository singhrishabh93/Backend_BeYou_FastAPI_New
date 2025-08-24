# BeYou API - FastAPI Backend

A REST API for managing positive affirmations built with FastAPI and MongoDB Atlas.

## 🚀 Features

- **CRUD Operations** for affirmations
- **MongoDB Atlas** integration
- **Automatic API documentation** with Swagger UI
- **CORS enabled** for frontend integration
- **Error handling** with proper HTTP status codes
- **Async/await** support for better performance

## 📋 Prerequisites

Before running this project, make sure you have:

- **Python 3.9+** installed
- **MongoDB Atlas** account and cluster set up
- **Git** (optional, for cloning)

## 🛠️ Installation & Setup

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd Backend_BeYou_FastAPI_New
```

### 2. Create and activate virtual environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the project root:
```bash
touch .env
```

Add your MongoDB Atlas connection details:
```env
MONGODB_URL=mongodb+srv://<username>:<password>@<cluster-name>.mongodb.net/?retryWrites=true&w=majority
DB_NAME=beyou_db
```

**To get your MongoDB connection string:**
1. Go to [MongoDB Atlas Dashboard](https://cloud.mongodb.com)
2. Click "Connect" on your cluster
3. Choose "Connect your application" 
4. Select Python driver
5. Copy the connection string and replace `<username>`, `<password>`, and `<cluster-name>`

### 5. Test MongoDB Connection (Optional)

Create `test_mongodb.py` to verify your database connection:
```python
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

async def test_connection():
    try:
        MONGODB_URL = os.getenv("MONGODB_URL")
        DB_NAME = os.getenv("DB_NAME", "beyou_db")
        
        print(f"Testing connection to MongoDB...")
        client = AsyncIOMotorClient(MONGODB_URL)
        
        await client.admin.command('ping')
        print("✅ Successfully connected to MongoDB!")
        
        db = client[DB_NAME]
        collections = await db.list_collection_names()
        print(f"✅ Available collections: {collections}")
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(test_connection())
```

Run the test:
```bash
python test_mongodb.py
```

## 🚀 Running the Application

### Development Mode
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at:
- **Main API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## 🐳 Docker Setup (Optional)

### Build and run with Docker:
```bash
# Build the image
docker build -t beyou-api .

# Run the container
docker run -p 8000:8000 beyou-api
```

## 📚 API Endpoints

### Base URL: `http://localhost:8000`

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| `GET` | `/` | Welcome message | None | `{"message": "Welcome to BeYou API"}` |
| `GET` | `/affirmations/` | Get all affirmations | None | Array of affirmations |
| `GET` | `/affirmations/{id}` | Get specific affirmation | None | Single affirmation object |
| `POST` | `/affirmations/` | Create new affirmation | `{"text": "string", "category": "string"}` | Created affirmation object |
| `DELETE` | `/affirmations/{id}` | Delete affirmation | None | `{"message": "Affirmation deleted successfully"}` |

### 📝 Request/Response Examples

#### Create Affirmation
```bash
curl -X POST "http://localhost:8000/affirmations/" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "I am worthy of love and respect",
    "category": "self-esteem"
  }'
```

**Response:**
```json
{
  "id": "a1b2c3d4e5",
  "text": "I am worthy of love and respect",
  "category": "self-esteem",
  "createdAt": "2025-08-24T12:00:00"
}
```

#### Get All Affirmations
```bash
curl "http://localhost:8000/affirmations/"
```

#### Delete Affirmation
```bash
curl -X DELETE "http://localhost:8000/affirmations/a1b2c3d4e5"
```

## 🧪 Testing the API

### Using Swagger UI (Recommended)
1. Start the server
2. Go to http://localhost:8000/docs
3. Try out endpoints interactively

### Using curl commands
```bash
# Test welcome endpoint
curl http://localhost:8000/

# Test get all affirmations
curl http://localhost:8000/affirmations/

# Test create affirmation
curl -X POST "http://localhost:8000/affirmations/" \
  -H "Content-Type: application/json" \
  -d '{"text": "I believe in myself", "category": "confidence"}'

# Test delete affirmation (replace with actual ID)
curl -X DELETE "http://localhost:8000/affirmations/{affirmation_id}"
```

## 📁 Project Structure

```
Backend_BeYou_FastAPI_New/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app configuration
│   ├── config.py            # Environment configuration
│   ├── database.py          # MongoDB connection
│   └── models/
│       ├── __init__.py
│       ├── affirmation.py   # Pydantic models
│       └── routers/
│           ├── __init__.py
│           └── affirmation.py  # API routes
├── .env                     # Environment variables
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
└── README.md               # This file
```

## 🔧 Troubleshooting

### Common Issues:

1. **503 Database Connection Error**
   - Check your MongoDB Atlas connection string
   - Verify your IP is whitelisted in MongoDB Atlas
   - Test connection with `python test_mongodb.py`

2. **Module Import Errors**
   - Ensure virtual environment is activated
   - Install dependencies: `pip install -r requirements.txt`

3. **Port Already in Use**
   - Change port: `uvicorn app.main:app --port 8001`
   - Or kill existing process: `lsof -ti:8000 | xargs kill -9`

### MongoDB Atlas Setup:
1. Create account at [MongoDB Atlas](https://cloud.mongodb.com)
2. Create a free cluster
3. Add your IP to Network Access (or use 0.0.0.0/0 for development)
4. Create database user with read/write permissions
5. Get connection string from "Connect" button

## 📦 Dependencies

```
fastapi==0.110.0
uvicorn==0.27.1
pymongo==4.6.2
motor==3.3.2
python-dotenv==1.0.1
pydantic==2.6.3
certifi
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Submit pull request

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**Rishabh Singh**
- GitHub: [singhrishabh93]
- Email: singhrishabh1670@gmail.com

---

**Happy Coding! 🎉**

For any issues or questions, please open an issue on GitHub or contact the maintainer.
