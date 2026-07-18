import subprocess
import sys

def handler(event, context):
    # Run Streamlit as a subprocess
    result = subprocess.run(
        [sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", "8000", "--server.address", "0.0.0.0"],
        capture_output=True,
        text=True
    )
    return {
        "statusCode": 200,
        "body": result.stdout
    }