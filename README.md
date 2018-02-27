
## Overview
This is a script and associated Docker tooling to help collect metrics from Pihole's API 
and send them to an Influxdb for trending / custom reporting.

## Usage

#### Using docker-compose

```bash
docker-compose up -d
```

####Using Docker:
```bash
docker build -t pihole_stats:latest .
docker run --restart=always -d -e METRIC_DELAY=10 \ 
       -e INFLUXDB_SERVER='192.168.2.10' \ 
       -e INFLUXDB_DATABASE='telegraf' \ 
       pihole_stats:latest
```

####Running manually under supervisor:
```bash
# See the supervisord.conf file in main source dir
1. Install supervisor. apt|yum|pip install supervisor
2. Add the pihole_stats.py script into /opt/scripts/ directory.
3. Run 'chmod +x /opt/scripts/pihole_stats.py'
4. Use the provided supervisord.conf file or add:

[program:pihole_stats]
command=python /opt/scripts/pihole_stats.py
stdout_logfile=/var/log/supervisor/%(program_name)s.log
stdout_errfile=/var/log/supervisor/%(program_name)s.log
startsecs=0
exitcodes=0,1
autostart=true
autorestart=false
priority=10
stdout_events_enabled=true
stderr_events_enabled=true

5. Restart supervisor on your system.
6. Confirm pihole_stats is running correctly using:

supervisorctl status
tail -f /var/log/supervisor/pihole_stats.log
```

#### Running as systemd service
https://linuxconfig.org/how-to-automatically-execute-shell-script-at-startup-boot-on-systemd-linux


## Troubleshooting

1. Confirm all needed python modules are installed. (requests and influxdb)
2. Manually run your command= section in the container by using docker exec.
3. Check the log files under /var/log/supervisor/ for errors.


## Author
sysadminnotes.ca

