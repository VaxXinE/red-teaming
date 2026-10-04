FROM python:3.13-slim
RUN pip install --no-cache-dir flask requests lxml
RUN useradd --uid 10001 --create-home labuser
WORKDIR /app
COPY app.py /app/app.py
USER 10001:10001
EXPOSE 8120
CMD ["python", "/app/app.py"]
