#!/bin/bash
set -e

# Log in to GitHub Container Registry if credentials are provided
if [ -n "$GITHUB_USERNAME" ] && [ -n "$GITHUB_TOKEN" ]; then
  echo "Logging in to GitHub Container Registry..."
  echo "$GITHUB_TOKEN" | docker login ghcr.io -u "$GITHUB_USERNAME" --password-stdin
  echo "Login successful!"
fi


# Execute the command passed to the script
exec "$@"
