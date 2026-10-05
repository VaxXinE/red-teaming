FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends openssh-server iproute2 procps && rm -rf /var/lib/apt/lists/*
RUN useradd -m -s /bin/bash operator && echo 'operator:Internal26!' | chpasswd && mkdir -p /run/sshd && printf 'CAPSTONE26-OBJECTIVE-ACHIEVED\n' > /home/operator/objective.txt && chown operator:operator /home/operator/objective.txt && chmod 600 /home/operator/objective.txt
RUN printf '\nPasswordAuthentication yes\nPermitRootLogin no\nAllowUsers operator\n' >> /etc/ssh/sshd_config
EXPOSE 22
CMD ["/usr/sbin/sshd","-D","-e"]
