# Use official Python image as base
FROM python:3.10-slim

# Set working directory
WORKDIR /bot

# Copy all bot files
COPY . /bot

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (fix TCP health check error)
EXPOSE 8080

# Run bot
CMD ["python", "bot.py"]
