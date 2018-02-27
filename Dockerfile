#
# Docker image for Pihole Statistics collector. This tool harvests the available metrics from the pihole api
# and sends them to an influxdb.
#
# Supported variables:
#
# HOSTNAME = "pihole"
# PIHOLE_API = "http://192.168.2.20/admin/api.php"
# INFLUXDB_SERVER = "192.168.2.5"
# INFLUXDB_PORT = 8086
# INFLUXDB_USERNAME = "telegraf"
# INFLUXDB_PASSWORD = "telegraf"
# INFLUXDB_DATABASE = "telegraf"
# DELAY = 10
# VERIFY_SSL = False
#
#  USAGE:
#
#     docker build -t pihole-stats .
#     docker run --restart=always \
#         -e PIHOLE_API="http://192.168.2.22/admin/api.php" \
#         -e INFLUXDB_SERVER="192.168.2.5" \
#         -d pihole-stats
#

FROM alpine:latest

RUN apk add --no-cache supervisor python3 python3-dev && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    pip3 install pytest requests influxdb && \
    mkdir -p /var/log/supervisor/ && \
    mkdir -p /opt/scripts/ && \
    rm -r /root/.cache

COPY supervisord.conf /etc/supervisord.conf
COPY pihole_stats.py /opt/scripts/pihole_stats.py

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
