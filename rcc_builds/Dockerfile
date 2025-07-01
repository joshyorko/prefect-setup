# Use Prefect’s Python 3.12 image
FROM prefecthq/prefect:3.2.9-python3.12

# Switch to root to install system packages
USER root

# 1) Install Node.js (v18) and basic tools
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       curl \
       gnupg \
       ca-certificates \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get update \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/*

# 2) Install Playwright, OS deps and browsers
RUN npm install -g playwright \
    && npx playwright install-deps \
    && npx playwright install --with-deps

# 3) Install RCC (Robocorp Command Center)
RUN curl -o /usr/local/bin/rcc https://downloads.robocorp.com/rcc/releases/v18.5.0/linux64/rcc \
    && chmod +x /usr/local/bin/rcc

# 4) Create non-root user and app directory
RUN useradd --create-home --shell /bin/bash appuser \
    && mkdir /app \
    && chown appuser:appuser /app

# 5) Copy your Robocorp environment files
WORKDIR /app
COPY conda.yaml robot.yaml ./

# 6) Drop to non-root and initialize holotree
USER appuser
RUN rcc holotree vars

# default workdir remains /app