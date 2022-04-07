# telegraf_test

Docker needs to be installed and in running state to execute this utiliy. 
For installtion and configuration of the docker please refer [link](https://docs.docker.com/get-docker/)

Agent
======

```
cd agent
chmod +x run.sh
./run.sh -c <agent-config-file-path>
```

Metric Sender
============

```
cd metric_sender
chmod +x run.sh
./run.sh -c <metric-sender-config-file-path>
```
Reference(s)
-------------
https://github.com/influxdata/telegraf