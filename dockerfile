# Use Python 3.12 image as base
FROM python:3.12

# Set working directory inside the container
WORKDIR /app

# Copy your Python script into the container
COPY game.py .

# Install dependencies (if any)
# RUN pip install -r requirements.txt

# Command to run your Python application
CMD ["python", "game.py"]
