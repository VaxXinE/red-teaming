FROM python:3.12-slim
WORKDIR /app
COPY app.py /app/app.py
RUN useradd -r -u 10001 app && chown -R app:app /app
USER app
EXPOSE 8081
CMD ["python","/app/app.py"]
