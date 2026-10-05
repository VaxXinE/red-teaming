FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends nmap curl jq openssh-client iproute2 netcat-openbsd procps ca-certificates && rm -rf /var/lib/apt/lists/*
RUN useradd -m -s /bin/bash analyst
USER analyst
WORKDIR /home/analyst
