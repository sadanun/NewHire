FROM python:3.12-slim

RUN pip install uv  

ENV PYTHONDONTWRITEBYTECODE=1 \
      PYTHONUNBUFFERED=1 \                                                                        
      UV_COMPILE_BYTECODE=1 \                                                                     
      UV_LINK_MODE=copy

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project 
COPY . .

CMD ["uv","run","python","manage.py","runserver","0.0.0.0:8000"]  