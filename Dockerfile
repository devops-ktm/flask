# Use official Python image
FROM python:3.13.3

# Set working directory
WORKDIR /app

# Copy all project files
COPY . /app

# Install Flask
RUN pip install --no-cache-dir flask

# Expose Flask default port
EXPOSE 5000

# Set environment variable to run app.py
ENV FLASK_APP=app.py

# Enable hot reloading and debug mode
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

# Command to run the app
CMD ["flask", "run"]
