#! /usr/bin/python
#
# To install and run the script as a service under SystemD.
# See: https://linuxconfig.org/how-to-automatically-execute-shell-script-at-startup-boot-on-systemd-linux

from __future__ import print_function

import os
import requests
import time

from influxdb import InfluxDBClient

HOSTNAME = os.getenv("PIHOLE_HOSTNAME", "pihole")
PIHOLE_API = os.getenv("PIHOLE_API", "http://192.168.2.20/admin/api.php")
INFLUXDB_SERVER = os.getenv("INFLUXDB_SERVER", "192.168.2.5")
INFLUXDB_PORT = os.getenv("INFLUXDB_PORT", 8086)
INFLUXDB_USERNAME = os.getenv("INFLUXDB_USERNAME", "telegraf")
INFLUXDB_PASSWORD = os.getenv("INFLUXDB_PASSWORD", "telegraf")
INFLUXDB_DATABASE = os.getenv("INFLUXDB_DATABASE", "telegraf")
DELAY = os.getenv("METRIC_DELAY", 10)
VERIFY_SSL = os.getenv("VERIFY_SSL", False)


class PiholeStats:

    def __init__(self):
        self.client = InfluxDBClient(INFLUXDB_SERVER, INFLUXDB_PORT,
                                     INFLUXDB_USERNAME, INFLUXDB_PASSWORD, INFLUXDB_DATABASE)

    def collector(self):

        while True:
            try:
                r = requests.get(PIHOLE_API, verify=VERIFY_SSL)
                data = r.json()

                json_body = [
                    {
                        "measurement": "piholestats." + HOSTNAME.replace(".", "_"),
                        "tags": {
                            "host": HOSTNAME
                        },
                        "fields": {
                            "domains_blocked": int(data['domains_being_blocked']),
                            "dns_queries_today": int(data['dns_queries_today']),
                            "ads_percentage_today": float(data['ads_percentage_today']),
                            "ads_blocked_today": int(data['ads_blocked_today']),
                            "unique_domains": int(data['unique_domains']),
                            "queries_forwarded": int(data['queries_forwarded']),
                            "queries_cached": int(data['queries_cached']),
                            "clients_ever_seen": int(data['clients_ever_seen']),
                            "unique_clients": int(data['unique_clients'])
                        }
                    }
                ]
                self.client.create_database(INFLUXDB_DATABASE)
                self.client.write_points(json_body)

                time.sleep(DELAY)
            except Exception as error:
                print(error)


if __name__ == '__main__':
    PiholeStats().collector()
