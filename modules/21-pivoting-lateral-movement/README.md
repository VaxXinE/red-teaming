# Module 21 - Pivoting & Lateral Movement

Module ini melanjutkan Active Directory sequence dengan fokus pada **network path dan controlled movement**: multi-homed hosts, routing, SSH local/dynamic/remote forwarding, SOCKS, ProxyJump, ProxyChains, route-based tunnels, Ligolo-ng/Chisel mental model, segmentation, lateral-movement reasoning, telemetry, evidence, dan cleanup.

## Learning goals

- Membaca interface/routing table dan mengidentifikasi pivot candidate.
- Membedakan SSH `-L`, `-D`, `-R`, dan `-J` berdasarkan arah listener dan connection origin.
- Memakai SOCKS + ProxyChains pada TCP secara terbatas dan memahami incompatibility dengan raw/pcap/UDP/ICMP workflows.
- Membedakan pivoting dari lateral movement dan mendokumentasikan execution-context transition.
- Memilih port-forward, SOCKS, jump host, atau route-based tunnel dengan blast radius minimum.
- Memahami Ligolo-ng dan Chisel sebagai alternatif tunnel tanpa menjadikannya default tool secara buta.
- Mengumpulkan telemetry/evidence dan melakukan cleanup yang dapat diverifikasi.

## Safety model

Hands-on utama hanya memakai Docker lab lokal yang terisolasi dan dummy credentials. Internal service tidak dipublish ke host; attacker container hanya terhubung ke external lab network, sedangkan jump host terhubung ke dua network. Tidak ada password spraying, credential dumping, hash replay, ticket abuse, atau remote-service abuse.

## Training credentials

Disposable lab only:

- jump: `pivot` / `Pivot21!`
- internal SSH: `student` / `Student21!`

Jangan reuse credential ini di sistem lain.

## Files

- `pdf/` - final learning module.
- `docx/` - editable source.
- `labs/` - Docker topology, helpers, activity log, topology report, dan evidence hashing.

## Core lab flow

```bash
cd labs
./pivot-lab.sh build
./pivot-lab.sh create
./segmentation-check.sh
./pivot-lab.sh shell
# lakukan exercise dari attacker container
./pivot-lab.sh cleanup
```

## References

- OpenSSH: https://man.openbsd.org/ssh.1
- Linux `ssh(1)`: https://man7.org/linux/man-pages/man1/ssh.1.html
- Linux `ip-route(8)`: https://man7.org/linux/man-pages/man8/ip-route.8.html
- ProxyChains-NG: https://github.com/rofl0r/proxychains-ng
- Ligolo-ng: https://docs.ligolo.ng/
- Chisel: https://github.com/jpillora/chisel
- Docker networking: https://docs.docker.com/engine/network/
