FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
COPY backend /app
COPY data /app/data
COPY control_room /app/control_room
ENV BTI_DATA_DIR=/app/data
ENV BTI_CONTROL_DIR=/app/control_room
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
