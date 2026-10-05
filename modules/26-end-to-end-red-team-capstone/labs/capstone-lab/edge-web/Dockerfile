FROM python:3.12-slim
WORKDIR /app
COPY app.py /app/app.py
RUN mkdir -p /app/files /secrets && printf 'Welcome to the Module 26 edge service.\n' > /app/files/welcome.txt && printf 'pivot:Pivot26!\n' > /secrets/jump-credential.txt && useradd -r -u 10001 app && chown -R app:app /app /secrets
USER app
EXPOSE 8080
CMD ["python","/app/app.py"]
