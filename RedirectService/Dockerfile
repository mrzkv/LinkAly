FROM python:3.13-bookworm

WORKDIR /app

COPY pyproject.toml .
RUN pip install uv && uv pip install . --system

COPY . .

ENV PYTHONPATH=/app

RUN chmod +x src/entrypoint.sh

ENTRYPOINT ["src/entrypoint.sh"]
