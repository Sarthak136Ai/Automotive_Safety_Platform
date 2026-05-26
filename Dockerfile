FROM python:3.10-slim

# Create a non-root user to comply with Hugging Face security requirements
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR /app

# Copy requirements and install dependencies
COPY --chown=user backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --user -r /app/requirements.txt

# Pre-download SpaCy lightweight english model
RUN python -m spacy download en_core_web_sm

# Copy codebase, database and precomputed artifacts with appropriate ownership
COPY --chown=user backend/ /app/backend/
COPY --chown=user src/ /app/src/
COPY --chown=user artifacts/ /app/artifacts/
COPY --chown=user data/ /app/data/
COPY --chown=user logs/ /app/logs/
COPY --chown=user autosentinel.db /app/autosentinel.db

ENV PYTHONPATH=/app

# Expose Hugging Face Space default port
EXPOSE 7860

# Start Uvicorn listening on mandatory port 7860
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "7860"]
