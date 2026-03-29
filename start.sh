#!/bin/bash

# Start the FastAPI backend in the background
echo "Starting FastAPI Backend on port 8001..."
uvicorn main:app --host 0.0.0.0 --port 8001 &

# Wait for backend to be ready
sleep 5

# Start the Streamlit frontend in the foreground
echo "Starting Streamlit Frontend on port ${PORT:-8000}..."
streamlit run streamlit_app.py --server.port ${PORT:-8000} --server.address 0.0.0.0