# 以 example-mcp 為預設映像：Streamable HTTP 監聽容器內 80 埠
FROM python:3.12-slim-bookworm

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    MCP_HOST=0.0.0.0 \
    MCP_PORT=80 \
    MCP_TRANSPORT=streamable-http

COPY example/pyproject.toml example/README.md /app/example/
COPY example/src /app/example/src

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir /app/example

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:80/health')" || exit 1

CMD ["example-mcp"]
