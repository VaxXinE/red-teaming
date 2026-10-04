FROM python:3.13-slim
RUN useradd --create-home --uid 10001 labuser \
 && pip install --no-cache-dir "Flask>=3.1,<4"
WORKDIR /app
COPY app.py /app/app.py
RUN mkdir -p /app/files && printf 'Welcome to Module 11.\n' > /app/files/welcome.txt \
 && chown -R labuser:labuser /app
USER labuser
EXPOSE 8111
CMD ["python", "/app/app.py"]
