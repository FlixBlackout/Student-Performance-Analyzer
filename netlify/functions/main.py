import sys
from pathlib import Path

# Add the project root to the Python path
# This is necessary for the lambda function to find the 'app' module
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from app import create_app
from mangum import Mangum

app = create_app()
handler = Mangum(app)
