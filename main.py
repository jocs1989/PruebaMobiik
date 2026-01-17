"""Main module for running the FastAPI app."""
import os

import uvicorn
from dotenv import load_dotenv

from config import config


load_dotenv(".env.dev") if os.environ.get("APP_ENV") == "local" else load_dotenv(".env")

PORT = config.PORT
HOST = config.HOST


def main():
    """Run the FastAPI app."""
    uvicorn.run(
        "src.app:app",
        host=HOST,
        port=int(PORT),
        reload=os.environ.get("APP_ENV") == "local",  # Activar reload en local,
        
    )


if __name__ == "__main__":
    main()
