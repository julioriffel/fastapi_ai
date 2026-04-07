FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim AS builder

# Set the working directory
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy project files
COPY pyproject.toml uv.lock ./

# Install dependencies into the system python (instead of a venv)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# ------------------------------------------------------------------------------
# Runtime stage
# ------------------------------------------------------------------------------
FROM python:3.14-rc-slim-trixie AS runtime

# Set the working directory
WORKDIR /app

# Copy the virtual environment from the builder
COPY --from=builder /app/.venv /app/.venv

# Copy the application code
COPY . .

# Make start.sh executable
RUN chmod +x start.sh

# Expose the port
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

# Command to run the application
CMD ["./start.sh"]
