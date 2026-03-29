#!/bin/bash

# Start the FastAPI backend in the background
echo "🚀 Starting FastAPI Backend on port 8000..."
uvicorn main:app --host 0.0.0.0 --port 8000 &

# Wait for backend to be ready (optional but recommended)
sleep 5

# Start the Streamlit frontend in the foreground
echo "🌍 Starting Streamlit Frontend on port 8501..."
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
