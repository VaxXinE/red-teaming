FROM debian:bookworm-slim
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    sudo cron gcc libc6-dev libcap2-bin procps iproute2 findutils util-linux passwd ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN useradd -m -s /bin/bash trainee \
    && echo 'trainee:training123' | chpasswd \
    && echo 'root:LabRootOnly!' | chpasswd
COPY suid_reader.c /tmp/suid_reader.c
COPY cap_reader.c /tmp/cap_reader.c
RUN gcc -O2 -Wall /tmp/suid_reader.c -o /usr/local/bin/suid-reader \
    && gcc -O2 -Wall /tmp/cap_reader.c -o /usr/local/bin/cap-reader \
    && chown root:root /usr/local/bin/suid-reader /usr/local/bin/cap-reader \
    && chmod 4755 /usr/local/bin/suid-reader \
    && chmod 0755 /usr/local/bin/cap-reader \
    && setcap cap_dac_read_search=ep /usr/local/bin/cap-reader \
    && rm -f /tmp/*.c
COPY lab-backup /usr/local/bin/lab-backup
RUN chown root:root /usr/local/bin/lab-backup && chmod 0755 /usr/local/bin/lab-backup \
    && printf 'trainee ALL=(root) NOPASSWD: /usr/local/bin/lab-backup *\n' > /etc/sudoers.d/mod16-lab \
    && chmod 0440 /etc/sudoers.d/mod16-lab
RUN mkdir -p /opt/lab-maintenance /opt/app \
    && printf 'FLAG{mod16_sudo_controlled_proof}\n' > /root/flag-sudo.txt \
    && printf 'FLAG{mod16_suid_controlled_proof}\n' > /root/flag-suid.txt \
    && printf 'FLAG{mod16_capability_controlled_proof}\n' > /root/flag-cap.txt \
    && printf 'FLAG{mod16_cron_controlled_proof}\n' > /root/flag-cron.txt \
    && printf 'FLAG{mod16_credential_controlled_proof}\n' > /root/flag-cred.txt \
    && chmod 0600 /root/flag-*.txt \
    && printf 'LAB_ADMIN_USER=root\nLAB_ADMIN_PASSWORD=LabRootOnly!\n' > /opt/app/config.env \
    && chown root:root /opt/app/config.env && chmod 0644 /opt/app/config.env
COPY task.sh /opt/lab-maintenance/task.sh
RUN chown root:trainee /opt/lab-maintenance/task.sh \
    && chmod 0775 /opt/lab-maintenance/task.sh \
    && printf '* * * * * root /opt/lab-maintenance/task.sh\n' > /etc/cron.d/mod16-maintenance \
    && chmod 0644 /etc/cron.d/mod16-maintenance
COPY entrypoint.sh /usr/local/bin/mod16-entrypoint
RUN chmod 0755 /usr/local/bin/mod16-entrypoint
ENTRYPOINT ["/usr/local/bin/mod16-entrypoint"]
