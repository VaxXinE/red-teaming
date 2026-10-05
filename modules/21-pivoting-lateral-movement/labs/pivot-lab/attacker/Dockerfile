FROM debian:bookworm-slim
RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
      openssh-client curl iproute2 iputils-ping netcat-openbsd nmap proxychains4 python3 ca-certificates procps \
 && rm -rf /var/lib/apt/lists/*
COPY proxychains.conf /etc/proxychains4.conf
CMD ["sleep", "infinity"]
