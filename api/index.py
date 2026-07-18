import subprocess
import sys
import os

def handler(event, context):
    # Run Streamlit as a subprocess
    result = subprocess.run(
        [sys.executable, "-m", "streamlit", "run", "src/main.py", 
         "--server.port", "8000", "--server.address", "0.0.0.0", 
         "--server.headless", "true"],
        capture_output=True,
        text=True
    )
    return {
        "statusCode": 200,
        "body": result.stdout
    }