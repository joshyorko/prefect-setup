FROM prefecthq/prefect:3-latest

# Install Docker CLI and the prefect-docker integration
RUN apt-get update && apt-get install -y docker.io && \
    pip install prefect-docker

# Clean up APT caches to reduce image size
RUN rm -rf /var/lib/apt/lists/*

# Create app directory if it doesn't exist
RUN mkdir -p /app

# Copy the entrypoint script into the image
COPY docker-entrypoint.sh /app/docker-entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /app/docker-entrypoint.sh

# Use the same entrypoint as the base image (your docker-entrypoint.sh will be invoked by the agent)
ENTRYPOINT ["/app/docker-entrypoint.sh"]