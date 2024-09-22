# Use an official Python runtime as a base image
FROM python:3.12-slim as base

# Set the working directory in the container
WORKDIR /covid_viz

# Install necessary system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip3 install poetry

# Copy the pyproject.toml and poetry.lock files first (for caching dependencies step)
COPY pyproject.toml poetry.lock ./

# Install dependencies via Poetry, without installing dev dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-dev

# Copy the rest of the application code into the container
COPY . .

# Expose the port that Streamlit uses
EXPOSE 8501

# Health check to ensure the application is running
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run the Streamlit app using Poetry to handle the environment
ENTRYPOINT ["poetry", "run", "streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]