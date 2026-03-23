# ============================================
# DOCKER DEMO — Dockerfile for Python App
# ============================================
# This file tells Docker HOW to build our image.
# Think of it as a recipe: step-by-step instructions.

# STEP 1: Start from a base image (Python 3.12, slim version = small size)
FROM python:3.12-slim

# STEP 2: Set working directory inside the container
# All commands after this run inside /app
WORKDIR /app

# STEP 3: Copy requirements FIRST (for layer caching)
# If requirements.txt doesn't change, Docker skips pip install on rebuild
COPY app/requirements.txt .

# STEP 4: Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# STEP 5: Copy the application code
COPY app/main.py .

# STEP 6: Tell Docker this container listens on port 8000
# (documentation only — doesn't actually open the port)
EXPOSE 8000

# STEP 7: Health check — Docker checks if our app is alive
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# STEP 8: The command to run when container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
