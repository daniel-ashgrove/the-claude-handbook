FROM python:3.13-slim
WORKDIR /app
COPY pyproject.toml uv.lock ./
COPY shop_orders ./shop_orders
RUN pip install --no-cache-dir uv==0.11.32 && uv sync --frozen --no-dev
ENV PATH="/app/.venv/bin:$PATH"
USER nobody
EXPOSE 8000
# Behind the platform's HTTPS proxy, which is the only thing that can reach port 8000
CMD ["uvicorn", "shop_orders.app:app", "--host", "0.0.0.0", "--port", "8000", \
     "--proxy-headers", "--forwarded-allow-ips=*"]
