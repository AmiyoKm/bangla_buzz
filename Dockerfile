# Stage 1: Build the dependencies
FROM python:3.9-slim as builder

WORKDIR /app

# Install uv for faster package installation
RUN pip install uv

# Copy requirements and install dependencies into a virtual environment
COPY requirements.txt .
RUN uv venv .venv && . .venv/bin/activate && uv pip install --no-cache-dir -r requirements.txt

# Stage 2: Create the final, smaller image
FROM python:3.9-slim

WORKDIR /app

# Install uv in the final image
RUN pip install uv

# Copy the virtual environment from the builder stage
COPY --from=builder /app/.venv .venv

# Copy the application source code and data
COPY src/ ./src/
COPY main.py main.py
COPY data data

# Add the virtual environment's bin to the PATH
ENV PATH="/app/.venv/bin:$PATH"

# Expose the port that Streamlit runs on
EXPOSE 8501

# Command to run the Streamlit app
# We also set the server address to 0.0.0.0 to allow external connections
CMD ["streamlit", "run", "src/dashboard.py", "--server.address=0.0.0.0"]
