# Use Python 3.9 as base image
FROM python:3.9

# Set the working directory
WORKDIR /bot

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all bot files into the container
COPY . .

# Expose port 8080 for health checks
EXPOSE 8080

# Run the bot and dummy server for health check
CMD ["bash", "-c", "python server.py & python bot.py"]
