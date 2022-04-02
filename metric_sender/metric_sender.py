import random
import time
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from telegraf.client import TelegrafClient


class TelegraphSender(object):
    def __init__(self, host='127.0.0.1', port=8092):
        self.ciient = TelegrafClient(host=host, port=port)
        self.loopup_dict = {
            'apache': 'send_apache_cpu_metrics',
            'iis_server': 'send_iis_server_cpu_metrics',
            'tomcat': 'send_tomcat_cpu_metrics',
            'sql_server': 'send_sql_server_cpu_metrics',
            'oracle': 'send_oracle_perf_metrics'
        }

    def send_apache_cpu_metrics(self, count=200):
        # https://github.com/influxdata/telegraf/tree/master/plugins/inputs/apache
        # apache,port=80,server=debian-stretch-apache BusyWorkers=1,BytesPerReq=0,BytesPerSec=0,CPUChildrenSystem=0,CPUChildrenUser=0,CPULoad=0.00995025,CPUSystem=0.01,CPUUser=0.01,ConnsAsyncClosing=0,ConnsAsyncKeepAlive=0,ConnsAsyncWriting=0,ConnsTotal=0,IdleWorkers=49,Load1=0.01,Load15=0,Load5=0,ParentServerConfigGeneration=3,ParentServerMPMGeneration=2,ReqPerSec=0.00497512,ServerUptimeSeconds=201,TotalAccesses=1,TotalkBytes=0,Uptime=201,scboard_closing=0,scboard_dnslookup=0,scboard_finishing=0,scboard_idle_cleanup=0,scboard_keepalive=0,scboard_logging=0,scboard_open=100,scboard_reading=0,scboard_sending=1,scboard_starting=0,scboard_waiting=49 1502489900000000000
        for i in range(count):
            self.ciient.metric('apache',
                               {
                                   'CPUChildrenSystem': 0,
                                   'CPUChildrenUser': 0,
                                   'CPULoad': random.uniform(10.5, 75.5),
                                   'CPUSystem': 0.01,
                                   'CPUUser': 0.01,
                               },
                               tags={
                                   'port': 80,
                                   "server": f"debian-stretch-apache-{i}"
                               }
                               )

    def send_tomcat_cpu_metrics(self, count=200):
        # https://github.com/influxdata/telegraf/tree/master/plugins/inputs/tomcat
        # tomcat_connector,host=N8-MBP,name=ajp-bio-8009 bytes_received=0i,bytes_sent=0i,current_thread_count=0i,current_threads_busy=0i,error_count=0i,max_threads=200i,max_time=0i,processing_time=0i,request_count=0i 1474663361000000000
        for i in range(count):
            self.ciient.metric('tomcat_connector',
                               {
                                   'bytes_received': random.randint(0, 10),
                                   'bytes_sent': random.randint(0, 10),
                                   'current_thread_count': random.randint(10, 20),
                                   'current_threads_busy': random.randint(0, 10),
                                   'error_count': 0,
                                   'max_threads': 0,
                                   'max_time': random.randint(5, 10),
                                   'processing_time': random.randint(0, 2),
                                   'request_count': random.randint(0, 2)
                               },
                               tags={
                                   'host': 'N8-MBP',
                                   "name": f"ajp-bio-8009-{i}"
                               }
                               )

    def send_sql_server_cpu_metrics(self, count=200):
        # https://github.com/zensqlmonitor/influxdb-sqlserver/blob/master/sqlscripts/getcpu.sql
        for i in range(count):
            self.ciient.metric('CPU',
                               {
                                   'SQLProcessUtilization': random.uniform(1.0, 99.0),
                                   'ExternalProcessUtilization': random.uniform(1.0, 50.0),
                                   'SystemIdle': random.uniform(1.0, 10.0),

                               },
                               tags={
                                   'type': 'CPU',
                                   "servername": f"sql-bio-8009-{i}"
                               }
                               )

    def send_iis_server_cpu_metrics(self, count=200):
        # https://github.com/influxdata/telegraf/blob/release-1.22/plugins/inputs/win_perf_counters/README.md
        for i in range(count):
            self.ciient.metric('win_cpu',
                               {
                                   '% Idle Time': random.uniform(1.0, 99.0),
                                   '% Interrupt Time': random.uniform(1.0, 50.0),
                                   '% Privileged Time': random.uniform(1.0, 10.0),
                                   '% User Time': random.uniform(1.0, 10.0),
                                   '% Processor Time': random.uniform(1.0, 10.0),

                               },
                               tags={
                                   'ObjectName': "Processor",
                                   "Instances": f"IIS+CPU-{i}"
                               }
                               )

    def send_oracle_perf_metrics(self, count=200):
        # https://github.com/twoinke/oracle-influxdb
        for i in range(count):
            tags = {
                'host': f"host-{i}",
                "db": "orcl",
                "session_state": random.choice(['WAITING', 'ON_CPU']),
                "wait_class": "Other",
                "event": random.choice(['os_thread_creation',
                                        'oracle_thread_bootstrap',
                                        'ADR_block_file_read']),
                "wait_time": 0,
                "session_state": random.choice(["WAITING",
                                                "NOT IN WAIT"])

            }
            if tags["session_state"] == "WAITING":
                tags['blocking_session_status'] = "UNKNOWN"
                tags["time_waited"] = str(random.randint(10040, 30000))
            self.ciient.metric('oracle_ash',
                               {
                                   'sample_id': str(random.randint(272130, 272139)),
                                   '% Interrupt Time': random.uniform(1.0, 50.0),
                                   '% Privileged Time': random.uniform(1.0, 10.0),
                                   '% User Time': random.uniform(1.0, 10.0),
                                   '% Processor Time': random.uniform(1.0, 10.0),

                               },
                               tags=tags
                               )

    def call_function(self, name, count):
        if name in self.loopup_dict.keys():
            if getattr(self, self.loopup_dict[name], None):
                getattr(self, self.loopup_dict[name])(count)


if __name__ == "__main__":
    # Parse command line arguments
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-t", "--type", default="apache",
                        help="type of the metric [apache | iisserver | oracle | tomcat | sqlserver]")
    parser.add_argument("-c", "--count", default=100, type=int, help="metric count to send")
    parser.add_argument("-s", "--sleep", default=60, type=int,
                        help="sleep suration betwwen seding metric in seconds (like 60 (1 min) or 300 (5 mins)")
    parser.add_argument("-i", "--iteration", default=10, type=int,
                        help="Nunmber of times metric to be sent")
    parser.add_argument("-a", "--host_port", default='127.0.0.1:8092', help='host_ip:port')
    args = vars(parser.parse_args())
    host, port = args['host_port'].split(':')
    print(f"host={host} port={port}")
    if args['iteration'] <= 0: args['iteration'] = 1
    if args['count'] <= 0: args['count'] = 1
    if args['sleep'] < 60:
        print (f"Setting to default sleep duration 60 seconds betwwen sendfing the metrics")
        args['iteration'] = 60

    tsender = TelegraphSender(host=host, port=int(port))
    if args['type'].lower() in tsender.loopup_dict.keys():
        time.sleep(random.uniform(1.0, 5.0))
        for i in range(args['iteration']):
            print(f"Iteration={i+1}: sending {args['type']} metrics....")
            tsender.call_function(args['type'].lower(), args['count'])
            print(f"sleeping for {args['sleep']} seconds..")
            time.sleep(args['sleep'])
    else:
        print(f"Unable to find metric generetor {args['type']}")

