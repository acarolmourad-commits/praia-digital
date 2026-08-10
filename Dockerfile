FROM python:3.11-slim

WORKDIR /app

COPY academy/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY academy/ ./academy/
COPY education/ ./education/
COPY static/ ./static/

ENV PYTHONPATH=/app
EXPOSE 8000

CMD ["uvicorn", "academy.main:app", "--host", "0.0.0.0", "--port", "8000"]
