FROM python:3.13-alpine
RUN addgroup -S lab && adduser -S -G lab -h /app lab
WORKDIR /app
COPY app.py /app/app.py
RUN chown -R lab:lab /app
USER lab
EXPOSE 8130
ENV BIND_HOST=0.0.0.0
CMD ["python", "/app/app.py"]
