
FROM python:3.9-slim-buster

# Set working directory
WORKDIR /flask-portfolio

# Copy requirements file first (for layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose port 5001
EXPOSE 5001

# Run the Flask app
CMD ["python3", "-m", "app"]

