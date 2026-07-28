FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt
COPY backend /app
COPY data /data
COPY control_room /control_room
ENV BTI_DATA_DIR=/data
ENV BTI_CONTROL_DIR=/control_room
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
