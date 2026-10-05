FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends openssh-server iproute2 procps gcc libc6-dev && rm -rf /var/lib/apt/lists/*
RUN useradd -m -s /bin/bash pivot && echo 'pivot:Pivot26!' | chpasswd && mkdir -p /run/sshd
COPY capstone-proof.c /tmp/capstone-proof.c
RUN gcc -O2 -Wall /tmp/capstone-proof.c -o /usr/local/bin/capstone-proof && chown root:root /usr/local/bin/capstone-proof && chmod 4755 /usr/local/bin/capstone-proof && rm -f /tmp/capstone-proof.c && printf 'TRAINING_INTERNAL_26\n' > /root/internal-token.txt && chmod 600 /root/internal-token.txt
RUN printf '\nPasswordAuthentication yes\nPermitRootLogin no\nAllowUsers pivot\n' >> /etc/ssh/sshd_config
EXPOSE 22
CMD ["/usr/sbin/sshd","-D","-e"]
