import sys
from pathlib import Path

# Add project root and backend folder to sys.path so modules can find each other correctly
project_root = str(Path(__file__).resolve().parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import the FastAPI application instance
from backend.app.main import app

# Vercel serverless handler
handler = app
