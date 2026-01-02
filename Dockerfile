FROM python:3.14-slim-bookworm

WORKDIR /spm

COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 80
COPY . .
CMD ["fastapi", "run", "./src/spm/main.py", "--port", "8000"]