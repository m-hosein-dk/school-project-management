FROM python:3.14-slim-bookworm@sha256:e8a1ad81a9fef9dc56372fb49b50818cac71f5fae238b21d7738d73ccae8f803

WORKDIR /spm

COPY requirements.txt .
RUN pip install -r requirements.txt

# NOTE: change the path in .env if you changed this one
RUN mkdir files

EXPOSE 18000
COPY . .
CMD ["fastapi", "run", "./src/spm/main.py", "--port", "18000"]