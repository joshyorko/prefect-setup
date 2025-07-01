FROM prefecthq/prefect:3.2.9-python3.12 AS builder

# Install system dependencies and Docker CLI
RUN apt-get update && apt-get install -y \
    docker.io \
    libgdk-pixbuf2.0-0 \
    libgtk-3-0 \
    libasound2 \
    libdbus-glib-1-2 \
    libxtst6 \
    xvfb \
    wget \
    # Playwright browser dependencies
    libglib2.0-0 \
    libnspr4 \
    libnss3 \
    libdbus-1-3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libatspi2.0-0 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libxcb1 \
    libxkbcommon0 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir prefect-docker playwright

# Install Playwright browsers
RUN playwright install

# Install RCC
RUN wget https://downloads.robocorp.com/rcc/releases/v18.5.0/linux64/rcc \
    && install rcc /usr/local/bin/rcc \
    && rm rcc

# --- Final image ---
FROM prefecthq/prefect:3.2.9-python3.12

# Copy installed tools and dependencies from builder
COPY --from=builder /usr/local/bin/rcc /usr/local/bin/rcc
COPY --from=builder /root/.cache/ms-playwright /root/.cache/ms-playwright

# Set holotree environment variables
ENV HOLOTREE_SHARED_HOME=/opt/robocorp/holotree \
    HOLOTREE_HOME=/opt/robocorp/holotree \
    RCC_HOLOTREE_SHARED_HOME=/opt/robocorp/holotree \
    RCC_HOLOTREE_HOME=/opt/robocorp/holotree

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser && \
    mkdir -p /app && chown appuser:appuser /app

# Copy environment files (adjust path as needed)
COPY conda.yaml /app/conda.yaml
COPY robot.yaml /app/robot.yaml

USER appuser
WORKDIR /app

RUN rcc holotree vars

