# Use a official Python image
FROM python:3.11

# Set workdir
WORKDIR /code

# Install system deps needed to build some Python packages and to install Poetry
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl build-essential gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry (installer will place poetry into /root/.local/bin)
ENV POETRY_VERSION=2.2.1
RUN curl -sSL https://install.python-poetry.org | python3 - --version $POETRY_VERSION

# Make poetry available on PATH
ENV PATH="/root/.local/bin:$PATH"

# Prevent Poetry from creating virtualenvs (install packages into container Python)
ENV POETRY_VIRTUALENVS_CREATE=false \ 
    POETRY_HOME="/root/.poetry" \
    POETRY_NO_INTERACTION=1 

# Copy only pyproject / poetry.lock first for better caching
# If you don't have a poetry.lock, the COPY will still work (poetry will resolve deps)
COPY pyproject.toml poetry.lock* /code/

# Install project dependencies
RUN poetry install --no-interaction --no-ansi --no-dev

# Copy app source
COPY ./app /code/app

# Expose port and run using uvicorn
EXPOSE 80

# Use uvicorn to serve the FastAPI app. Adjust the module path if your ASGI app is not app.main:app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

# Build the Docker image
# docker build -t myimage .

# Run the container
# docker run -d --name mycontainer -p 80:80 myimage 