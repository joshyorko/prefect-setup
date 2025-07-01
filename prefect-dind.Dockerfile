FROM prefecthq/prefect:3-latest

# Install Docker CLI, prefect-docker, Playwright dependencies, and RCC
RUN apt-get update && apt-get install -y \
    docker.io \
    libgdk-pixbuf2.0-0 \
    libgtk-3-0 \
    libasound2 \
    libdbus-glib-1-2 \
    libxtst6 \
    xvfb \
    wget && \
    pip install prefect-docker playwright && \
    playwright install && \
    wget https://downloads.robocorp.com/rcc/releases/v18.5.0/linux64/rcc && \
    install rcc /usr/local/bin/rcc && \
    rm rcc

# Set holotree environment variables
ENV HOLOTREE_SHARED_HOME=/opt/robocorp/holotree
ENV HOLOTREE_HOME=/opt/robocorp/holotree
ENV RCC_HOLOTREE_SHARED_HOME=/opt/robocorp/holotree
ENV RCC_HOLOTREE_HOME=/opt/robocorp/holotree

# Clean up APT caches to reduce image size
RUN rm -rf /var/lib/apt/lists/*

# Create app directory if it doesn't exist
RUN mkdir -p /app
ARG ROBOT_PATH
COPY ${ROBOT_PATH}/conda.yaml /app/conda.yaml
COPY ${ROBOT_PATH}/robot.yaml /app/robot.yaml
WORKDIR /app
RUN rcc holotree vars
# Copy the entrypoint script into the image
COPY docker-entrypoint.sh /app/docker-entrypoint.sh

# Make the entrypoint script executable
RUN chmod +x /app/docker-entrypoint.sh

# Use the same entrypoint as the base image (your docker-entrypoint.sh will be invoked by the agent)
ENTRYPOINT ["/app/docker-entrypoint.sh"]