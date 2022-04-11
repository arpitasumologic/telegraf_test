import random
import time
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from telegraf.client import TelegrafClient

def merge(dict1, dict2):
    return {**dict1, **dict2}

class TelegraphSender(object):
    def __init__(self, host='127.0.0.1', port=8092):
        self.ciient = TelegrafClient(host=host, port=port)
        self.loopup_dict = {
            'apache_cpu': 'send_apache_cpu_metrics',
            'iis_server_cpu': 'send_iis_server_cpu_metrics',
            'tomcat_cpu': 'send_tomcat_cpu_metrics',
            'tomcat_memory': 'send_tomcat_memory_metrics',
            'sql_server_cpu': 'send_sql_server_cpu_metrics',
            'oracle_cpu': 'send_oracle_perf_metrics'
        }

    def send_apache_cpu_metrics(self, count=200):
        # https://github.com/influxdata/telegraf/tree/master/plugins/inputs/apache
        # apache,port=80,server=debian-stretch-apache BusyWorkers=1,BytesPerReq=0,BytesPerSec=0,CPUChildrenSystem=0,CPUChildrenUser=0,CPULoad=0.00995025,CPUSystem=0.01,CPUUser=0.01,ConnsAsyncClosing=0,ConnsAsyncKeepAlive=0,ConnsAsyncWriting=0,ConnsTotal=0,IdleWorkers=49,Load1=0.01,Load15=0,Load5=0,ParentServerConfigGeneration=3,ParentServerMPMGeneration=2,ReqPerSec=0.00497512,ServerUptimeSeconds=201,TotalAccesses=1,TotalkBytes=0,Uptime=201,scboard_closing=0,scboard_dnslookup=0,scboard_finishing=0,scboard_idle_cleanup=0,scboard_keepalive=0,scboard_logging=0,scboard_open=100,scboard_reading=0,scboard_sending=1,scboard_starting=0,scboard_waiting=49 1502489900000000000
        for i in range(count):
            self.ciient.metric('apache',
                               {
                                   'CPUChildrenSystem': random.uniform(0.0, 0.1),
                                   'CPUChildrenUser': random.uniform(0.0, 0.1),
                                   'CPULoad': random.uniform(10.5, 75.5),
                                   'CPUSystem': random.uniform(0.0, 0.01),
                                   'CPUUser': random.uniform(0.0, 0.02),
                                   'DurationPerReq': random.uniform(0.01, 0.02),
                                   'IdleWorkers': random.uniform(0.01, 0.05),
                                   'apache_Load1': random.uniform(0.1, 30.0),
                                   'apache_Load5': random.uniform(0.1, 30.0),
                                   'apache_Load15': random.uniform(0.1, 30.0),
                                   'ParentServerConfigGeneration': random.uniform(0.1, 30.0),
                                   'ParentServerMPMGeneration': random.uniform(0.1, 30.0),
                                   'ReqPerSec': random.uniform(0.1, 30.0),
                                   'ServerUptimeSeconds': random.randint(1, 600000),
                                   'TotalAccesses': random.randint(3000, 8000),
                                   'TotalDuration': random.uniform(60.0, 70.0),
                                   'TotalkBytes': random.randint(800000, 900000),
                                   'Uptime': random.randint(600000, 700000),
                                   'scboard_closing': random.uniform(600000.0, 700000.0),
                                   'scboard_dnslookup': random.uniform(500000.0, 600000.0),
                                   'scboard_finishing': random.uniform(600000.0, 700000.0),
                                   'scboard_idle_cleanup': random.uniform(600000.0, 700000.0),
                                   'scboard_keepalive': random.uniform(600000.0, 700000.0),
                                   'scboard_logging': random.uniform(600000.0, 700000.0),
                                   'scboard_open': random.uniform(600000.0, 700000.0),
                                   'scboard_reading': random.uniform(600000.0, 700000.0),
                                   'scboard_sending': random.uniform(600000.0, 700000.0),
                                   'scboard_starting': random.uniform(600000.0, 700000.0),
                                   'scboard_waiting': random.uniform(600000.0, 700000.0),
                               },
                               tags={
                                   'port': 80,
                                   "server": f"debian-stretch-apache-{i}",
                                   "environment": "prod",
                                   "component": "webserver",
                                   "webserver_system": "apache",
                                   "webserver_farm": f"my-test-firm-{random.randint(0, 1)}",
                                   "source_category": "Labs/apache"

                               }
                               )

    def send_tomcat_cpu_metrics(self, count=200):
        # https://github.com/influxdata/telegraf/tree/master/plugins/inputs/tomcat
        # tomcat_connector,host=N8-MBP,name=ajp-bio-8009 bytes_received=0i,bytes_sent=0i,current_thread_count=0i,current_threads_busy=0i,error_count=0i,max_threads=200i,max_time=0i,processing_time=0i,request_count=0i 1474663361000000000
        for i in range(count):
            self.ciient.metric('tomcat_jmx_GlobalRequestProcessor',
                               {
                                   'bytesReceived': random.randint(0, 10),
                                   'bytesSent': random.randint(0, 10),
                                   'processingTime': random.uniform(10.0, 20.0),
                                   'requestCount': random.randint(0, 10),
                                   'errorCount': random.randint(0, 10),
                               },
                               tags={
                                   'host': f"N8-MBP-{i}",
                                   "name": f"GlobalRequestProcessor",
                                   "environment": "prod",
                                   "component": "webserver",
                                   "webserver_system": "tomcat",
                                   "webserver_farm": f"my-test-firm-{random.randint(0, 1)}",
                                   "source_category": "Labs/tomcat"

                               }
                               )
            self.ciient.metric('tomcat_jmx_JspMonitor',
                               {
                                   'jspCount': random.randint(0, 10),
                                   'jspReloadCount': random.randint(0, 10),
                                   'jspUnloadCount': random.randint(0, 10),
                               },
                               tags={
                                   'host': f"N8-MBP-{i}",
                                   "name": f"JspMonitor",
                                   "environment": "prod",
                                   "component": "webserver",
                                   "webserver_system": "tomcat",
                                   "webserver_farm": f"my-test-firm-{random.randint(0, 1)}",
                                   "source_category": "Labs/tomcat"

                               }
                               )
            self.ciient.metric('tomcat_jmx_OperatingSystem',
                               {
                                   'AvailableProcessors': random.randint(1, 10),
                                   'FreePhysicalMemorySize': random.randint(1024, 2048),
                                   'FreeSwapSpaceSize': random.randint(512, 1024),
                                   'TotalPhysicalMemorySize': random.randint(1024, 2048),
                                   'TotalSwapSpaceSize': random.randint(512, 1024),
                                   'ProcessCpuLoad': random.uniform(10.0, 20.0),
                                   'SystemCpuLoad': random.uniform(10.0, 20.0),
                                   'SystemLoadAverage': random.uniform(10.0, 20.0)

                               },
                               tags={
                                   'host': f"N8-MBP-{i}",
                                   "name": f"OperatingSyste",
                                   "environment": "prod",
                                   "component": "webserver",
                                   "webserver_system": "tomcat",
                                   "webserver_farm": f"my-test-firm-{random.randint(0, 1)}",
                                   "source_category": "Labs/tomcat"

                               }
                               )
            self.ciient.metric('tomcat_jmx_Servlet',
                               {
                                   'errorCount': random.randint(1, 10),
                                   'requestCount': random.randint(1, 50),
                                   'processingTime': random.uniform(10.0, 20.0),

                               },
                               tags={
                                   'host': f"N8-MBP-{i}",
                                   "name": f"Servlet",
                                   "environment": "prod",
                                   "component": "webserver",
                                   "webserver_system": "tomcat",
                                   "webserver_farm": f"my-test-firm-{random.randint(0, 1)}",
                                   "source_category": "Labs/tomcat"

                               }
                               )
            self.ciient.metric('tomcat_jmx_ThreadPool',
                               {
                                   'currentThreadCount': random.randint(10, 50),
                                   'currentThreadsBusy': random.randint(1, 9),
                                   'maxThread': random.randint(100, 120)

                               },
                               tags={
                                   'host': f"N8-MBP-{i}",
                                   "name": f"ThreadPool",
                                   "environment": "prod",
                                   "component": "webserver",
                                   "webserver_system": "tomcat",
                                   "webserver_farm": f"my-test-firm-{random.randint(0, 1)}",
                                   "source_category": "Labs/tomcat"

                               }
                               )

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
                                   'host': f"N8-MBP-{i}",
                                   "name": f"ajp-bio-8009-{i}",
                                   "environment": "prod",
                                   "component": "webserver",
                                   "webserver_system": "tomcat",
                                   "webserver_farm": f"my-test-firm-{random.randint(0, 1)}",
                                   "source_category": "Labs/tomcat"

                               }
                               )

    def send_tomcat_memory_metrics(self, count=200):
        # https://github.com/influxdata/telegraf/tree/master/plugins/inputs/tomcat
        # tomcat_connector,host=N8-MBP,name=ajp-bio-8009 bytes_received=0i,bytes_sent=0i,current_thread_count=0i,current_threads_busy=0i,error_count=0i,max_threads=200i,max_time=0i,processing_time=0i,request_count=0i 1474663361000000000
        for i in range(count):
            self.ciient.metric('tomcat_jmx_jvm_garbage_collector',
                               {
                                   'CollectionCount': random.randint(50, 10000),
                                   'CollectionTime': random.uniform(0.5, 0.6),
                               },
                               tags={
                                   'host': f"N8-MBP-{i}",
                                   "name": f"garbage_collector",
                                   "environment": "prod",
                                   "component": "webserver",
                                   "webserver_system": "tomcat",
                                   "webserver_farm": f"my-test-firm-{random.randint(0, 1)}",
                                   "source_category": "Labs/tomcat"

                               }
                               )

            self.ciient.metric('tomcat_jvm_memory',
                               {
                                   'free': random.randint(50, 10000),
                                   'total': random.choice([32000, 64000]),
                                   'max': random.randint(10000, 30000),
                               },
                               tags={
                                   'host': f"N8-MBP-{i}",
                                   "name": f"ajp-bio-8009-{i}",
                                   "environment": "prod",
                                   "component": "webserver",
                                   "webserver_system": "tomcat",
                                   "webserver_farm": f"my-test-firm-{random.randint(0, 1)}",
                                   "source_category": "Labs/tomcat"

                               }
                               )
            for type in ['HeapMemoryUsage', 'NonHeapMemoryUsage', 'CollectionUsage', 'PeakUsage', 'Usage']:
                self.ciient.metric(f"tomcat_jmx_jvm_memory_pool_{type}",
                                   {
                                       'commited': random.randint(11534336, 21534336),
                                       'init': random.randint(2228224, 3228224),
                                       'max': random.randint(35258368, 45258368),
                                       'used': random.randint(1941200, 2941200)
                                   },
                                   tags={
                                       'host': 'N8-MBP-{i}',
                                       "name": f"ajp-bio-8009-{i}",
                                       "type": type,
                                       "environment": "prod",
                                       "component": "webserver",
                                       "webserver_system": "tomcat",
                                       "webserver_farm": f"my-test-firm-{random.randint(0, 1)}",
                                       "source_category": "Labs/tomcat"

                                   }
                                   )
            self.ciient.metric('tomcat_jvm_memorypool',
                               {
                                   'commited': random.randint(11534336, 21534336),
                                   'init': random.randint(2228224, 3228224),
                                   'max': random.randint(35258368, 45258368),
                                   'used': random.randint(1941200, 2941200)
                               },
                               tags={
                                   'host': f"N8-MBP-{i}",
                                   "name": f"ajp-bio-8009-{i}",
                                   "type": random.choice(['Heap', 'Non-Heap']),
                                   "environment": "prod",
                                   "component": "webserver",
                                   "webserver_system": "tomcat",
                                   "webserver_farm": f"my-test-firm-{random.randint(0, 1)}",
                                   "source_category": "Labs/tomcat"

                               }
                               )

    def send_iis_server_cpu_metrics(self, count=200):
        # https://github.com/influxdata/telegraf/blob/release-1.22/plugins/inputs/win_perf_counters/README.md
        for i in range(count):
            self.ciient.metric('win_cpu',
                               {
                                   'IdleTime': random.uniform(1.0, 99.0),
                                   'InterruptTime': random.uniform(1.0, 50.0),
                                   'PrivilegedTime': random.uniform(1.0, 10.0),
                                   'UserTime': random.uniform(1.0, 10.0),
                                   'ProcessorTime': random.uniform(1.0, 10.0),

                               },
                               tags={
                                   'ObjectName': "Processor",
                                   "host": f"IIS+CPU-{i}",
                                   "Instances": f"IIS+CPU-{i}",
                                   "environment": "prod",
                                   "component": "webserver",
                                   "webserver_system": "iis",
                                   "webserver_farm": f"my-test-firm-{random.randint(0, 1)}",
                                   "source_category": "Labs/iis"
                               }
                               )

    def send_sql_server_cpu_metrics(self, count=200):
        # https://github.com/zensqlmonitor/influxdb-sqlserver/blob/master/sqlscripts/getcpu.sql
        # https://gitlab.flux.utah.edu/emulab/telegraf/-/blob/3ef28e332fe8dba93fd873542c16effb6cb4e54c/plugins/inputs/sqlserver/sqlserver.go
        for i in range(count):
            common_tags = {
                "sql_instance": f"sql-bio-8009-{i}",
                "host": f"sql-bio-8009-{i}",
                "servername": f"sql-bio-8009-{i}",
                "environment": "prod",
                "component": "database",
                "database_system": "sqlserver",
                "database_farm": f"my-sqlserver-firm-{random.randint(0, 1)}",
                "cluster": f"my-sql-cluster-{random.randint(0, 1)}",
                "source_category": "Labs/sqlserver"

            }
            self.ciient.metric('sqlserver_performance',
                               {
                                   'value': random.randint(50, 75)

                               },
                               tags=common_tags
                               )
            self.ciient.metric('sqlserver_memory_clerks',
                               {
                                   'size_kb': random.randint(24000, 25000),

                               },
                               tags=merge(common_tags, {'clerk_type': 0})
                            )
            self.ciient.metric('sqlserver_waitstats',
                               {
                                   'max_wait_time_ms': random.uniform(0.01, 0.02),
                                   'resource_wait_ms':random.uniform(0.01, 0.02),
                                   'signal_wait_time_ms': random.uniform(0.01, 0.02),
                                   'wait_time_ms': random.uniform(0.01, 0.02),
                                   'waiting_tasks_count':random.randint(0, 5)

                               },
                               tags=merge(common_tags, {'wait_category': random.choice(['CPU', 'MEMORY', 'OTHER'])})
                               )
            self.ciient.metric('volume_space',
                               {
                                   'available_space_bytes': random.randint(24000, 25000),
                                   'total_space_bytes':random.randint(26000, 27000),
                                   'used_space_bytes':random.randint(100, 1000),

                               },
                               tags=common_tags
                               )
            self.ciient.metric('sqlserver_requests',
                               {
                                   'logical_reads': random.randint(24000, 25000),
                                   'open_transaction': random.randint(26000, 27000),
                                   'requests_percent_complete': random.uniform(50, 70),
                                   'total_elapsed_time_ms':random.uniform(0.01, 0.02),
                                   'wait_time_ms':random.uniform(0.01, 0.02),
                                   'writes': random.randint(24000, 25000)

                               },
                               tags=merge (common_tags,
                                {'request_id': random.randint(30000, 40000),
                                 'session_id': random.randint(1555,1600),
                                 'blocking_session_id':random.randint(1555,1600)})
                               )
            self.ciient.metric('sqlserver_database_io',
                               {
                                   'read_latency_ms': random.uniform(0.001, 0.003),
                                   'reads': random.randint(2000, 3000),
                                   'read_bytes': random.randint(20000, 30000),
                                   'write_latency_ms': random.uniform(0.004, 0.005),
                                   'writes': random.randint(1000, 2000),
                                   'write_bytes': random.randint(30000, 40000)

                               },
                               tags=merge(common_tags, {'database_name': f"db_{i}"})
                               )
            self.ciient.metric('sqlserver_server_properties',
                               {
                                   'db_online': random.randint(0, 5),
                                   'db_restoring': random.randint(0, 5),
                                   'db_recovering': random.randint(0, 5),
                                   'db_recoveryPending': random.randint(0, 5),
                                   'db_suspect': random.randint(0, 5),
                                   'db_offline': random.randint(0, 5),
                                   'cpu_count': random.randint(1,32),
                                   'server_memory': random.randint(24000, 48000),
                                   'uptime': random.randint(24000, 48000)
                               },
                               tags=merge(common_tags, {'database_name': f"db_{i}"})
                               )

    def send_oracle_perf_metrics(self, count=200):
        # https://github.com/bonitoo-io/telegraf-input-oracle/blob/main/README.md
        wait_event_dict = {
            'Network': 'SQL*Net_message_to_client',
            'Other': 'asynch_descriptor_resize',
            'System_I/O': random.choice([
                'log_file_parallel_write',
                'control_file_sequential_read',
                'control_file_parallel_write'
            ])
        }

        for i in range(count):
            common_tags = {
                "instance": f"XE-{i}",
                "host": f"XE-{i}",
                "environment": "prod",
                "component": "database",
                "database_system": "oracle",
                "database_farm": f"my-oracle-firm-{random.randint(0, 1)}",
                "cluster": f"my-oracle-cluster-{random.randint(0, 1)}",
                "source_category": "Labs/oracle"

            }
            self.ciient.metric('oracle_connectioncount',
                               {
                                   'metric_value': random.randint(20, 50),
                               },
                               tags=merge(common_tags, {"metric_name": "ACTIVE"}),
                               )
            for tbs_name in ['SYSAUX', 'SYSTEM', 'TEMP', 'UNDOTBS1', 'USERS']:
                self.ciient.metric('oracle_tablespaces',
                                   {
                                       'free_space_mb,': random.randint(250, 25549),
                                       'max_size_mb': random.randint(600, 26154),
                                       'percent_used': random.uniform(20.0, 50.0),
                                       'used_space_mb': random.randint(5, 60)

                                   },
                                   tags=merge(common_tags, {"tbs_name": tbs_name})
                                   )
            for wait_class in ['SYSAUX', 'SYSTEM', 'TEMP', 'UNDOTBS1', 'USERS', 'Configuration', 'Network', 'Other',
                               'Scheduler', 'System_I/O', 'User_I/O']:
                self.ciient.metric('oracle_wait_class',
                                   {
                                       'wait_value,': random.uniform(0.0, 0.25)

                                   },
                                   tags=merge(common_tags, {"wait_class": wait_class})

                                   )

            for wait_event in wait_event_dict.keys():
                self.ciient.metric('oracle_wait_event',
                                   {
                                       'count,': random.randint(5, 20),
                                       'latency': random.uniform(0.002, 0.005)

                                   },
                                   tags=merge(common_tags,
                                              {"wait_class": wait_event, "wait_event": wait_event_dict[wait_event]})

                                   )

            self.ciient.metric('oracle_status',
                               {
                                   'metric_value': random.randint(0, 1),
                               },
                               tags=merge(common_tags, {"metric_name": "database_status"})
                               )
            for metric_name in [
                'Buffer_Cache_Hit_Ratio',
                'Memory_Sorts_Ratio',
                'Redo_Allocation_Hit_Ratio',
                'User_Transaction_Per_Sec',
                'Physical_Reads_Per_Sec',
                'Physical_Reads_Per_Txn',
                'Physical_Writes_Per_Sec',
                'Physical_Writes_Per_Txn',
                'Physical_Reads_Direct_Per_Sec',
                'Physical_Reads_Direct_Per_Txn',
                'Physical_Writes_Direct_Per_Sec',
                'Physical_Writes_Direct_Per_Txn',
                'Physical_Reads_Direct_Lobs_Per_Sec',
                'Physical_Reads_Direct_Lobs_Per_Txn',
                'Physical_Writes_Direct_Lobs_Per_Sec',
                'Physical_Writes_Direct_Lobs__Per_Txn',
                'Redo_Generated_Per_Sec',
                'Redo_Generated_Per_Txn',
                'Logons_Per_Sec',
                'Logons_Per_Txn',
                'Open_Cursors_Per_Sec',
                'Open_Cursors_Per_Txn',
                'User_Commits_Per_Sec',
                'User_Commits_Percentage',
                'User_Rollbacks_Per_Sec',
                'User_Rollbacks_Percentage',
                'User_Calls_Per_Sec',
                'User_Calls_Per_Txn',
                'Recursive_Calls_Per_Sec',
                'Recursive_Calls_Per_Txn',
                'Logical_Reads_Per_Sec',
                'Logical_Reads_Per_Txn',
                'DBWR_Checkpoints_Per_Sec',
                'Background_Checkpoints_Per_Sec',
                'Redo_Writes_Per_Sec',
                'Redo_Writes_Per_Txn',
                'Long_Table_Scans_Per_Sec',
                'Long_Table_Scans_Per_Txn',
                'Total_Table_Scans_Per_Sec',
                'Total_Table_Scans_Per_Txn',
                'Full_Index_Scans_Per_Sec',
                'Full_Index_Scans_Per_Txn',
                'Total_Index_Scans_Per_Sec',
                'Total_Index_Scans_Per_Txn',
                'Total_Parse_Count_Per_Sec',
                'Total_Parse_Count_Per_Txn',
                'Hard_Parse_Count_Per_Sec',
                'Hard_Parse_Count_Per_Txn',
                'Parse_Failure_Count_Per_Sec',
                'Parse_Failure_Count_Per_Txn',
                'Cursor_Cache_Hit_Ratio',
                'Disk_Sort_Per_Sec',
                'Disk_Sort_Per_Txn',
                'Rows_Per_Sort',
                'Execute_Without_Parse_Ratio',
                'Soft_Parse_Ratio',
                'User_Calls_Ratio',
                'Host_CPU_Utilization_(%)',
                'Network_Traffic_Volume_Per_Sec',
                'Enqueue_Timeouts_Per_Sec',
                'Enqueue_Timeouts_Per_Txn',
                'Enqueue_Waits_Per_Sec',
                'Enqueue_Waits_Per_Txn',
                'Enqueue_Deadlocks_Per_Sec',
                'Enqueue_Deadlocks_Per_Txn',
                'Enqueue_Requests_Per_Sec',
                'Enqueue_Requests_Per_Txn',
                'DB_Block_Gets_Per_Sec',
                'DB_Block_Gets_Per_Txn',
                'Consistent_Read_Gets_Per_Sec',
                'Consistent_Read_Gets_Per_Txn',
                'DB_Block_Changes_Per_Sec',
                'DB_Block_Changes_Per_Txn',
                'Consistent_Read_Changes_Per_Sec',
                'Consistent_Read_Changes_Per_Txn',
                'CPU_Usage_Per_Sec',
                'CPU_Usage_Per_Txn',
                'CR_Blocks_Created_Per_Sec',
                'CR_Blocks_Created_Per_Txn',
                'CR_Undo_Records_Applied_Per_Sec',
                'CR_Undo_Records_Applied_Per_Txn',
                'User_Rollback_UndoRec_Applied_Per_Sec',
                'User_Rollback_Undo_Records_Applied_Per_Txn',
                'Leaf_Node_Splits_Per_Sec',
                'Leaf_Node_Splits_Per_Txn',
                'Branch_Node_Splits_Per_Sec',
                'Branch_Node_Splits_Per_Txn',
                'PX_downgraded_1_to_25%_Per_Sec',
                'PX_downgraded_25_to_50%_Per_Sec',
                'PX_downgraded_50_to_75%_Per_Sec',
                'PX_downgraded_75_to_99%_Per_Sec',
                'PX_downgraded_to_serial_Per_Sec',
                'Physical_Read_Total_IO_Requests_Per_Sec',
                'Physical_Read_Total_Bytes_Per_Sec',
                'GC_CR_Block_Received_Per_Second',
                'GC_CR_Block_Received_Per_Txn',
                'GC_Current_Block_Received_Per_Second',
                'GC_Current_Block_Received_Per_Txn',
                'Global_Cache_Average_CR_Get_Time',
                'Global_Cache_Average_Current_Get_Time',
                'Physical_Write_Total_IO_Requests_Per_Sec',
                'Global_Cache_Blocks_Corrupted',
                'Global_Cache_Blocks_Lost',
                'Current_Logons_Count',
                'Current_Open_Cursors_Count',
                'User_Limit_%',
                'SQL_Service_Response_Time',
                'Database_Wait_Time_Ratio',
                'Database_CPU_Time_Ratio',
                'Response_Time_Per_Txn',
                'Row_Cache_Hit_Ratio',
                'Row_Cache_Miss_Ratio',
                'Library_Cache_Hit_Ratio',
                'Library_Cache_Miss_Ratio',
                'Shared_Pool_Free_%',
                'PGA_Cache_Hit_%',
                'Process_Limit_%',
                'Session_Limit_%',
                'Executions_Per_Txn',
                'Executions_Per_Sec',
                'Executions_Per_Sec',
                'Database_Time_Per_Sec',
                'Physical_Write_Total_Bytes_Per_Sec',
                'Physical_Read_IO_Requests_Per_Sec',
                'Physical_Read_Bytes_Per_Sec',
                'Physical_Write_IO_Requests_Per_Sec',
                'Physical_Write_Bytes_Per_Sec',
                'DB_Block_Changes_Per_User_Call',
                'DB_Block_Gets_Per_User_Call',
                'Executions_Per_User_Call',
                'Logical_Reads_Per_User_Call',
                'Total_Sorts_Per_User_Call',
                'Total_Table_Scans_Per_User_Call',
                'Current_OS_Load',
                'Streams_Pool_Usage_Percentage',
                'PQ_QC_Session_Count',
                'PQ_Slave_Session_Count',
                'Queries_parallelized_Per_Sec',
                'DML_statements_parallelized_Per_Sec',
                'DDL_statements_parallelized_Per_Sec',
                'PX_operations_not_downgraded_Per_Sec',
                'Session_Count',
                'Average_Synchronous_Single-Block_Read_Latency',
                'I/O_Megabytes_per_Second',
                'I/O_Requests_per_Second',
                'Average_Active_Sessions',
                'Active_Serial_Sessions',
                'Active_Parallel_Sessions',
                'Captured_user_calls',
                'Replayed_user_calls',
                'Workload_Capture_and_Replay_status',
                'Background_CPU_Usage_Per_Sec',
                'Background_Time_Per_Sec',
                'Host_CPU_Usage_Per_Sec',
                'Cell_Physical_IO_Interconnect_Bytes',
                'Temp_Space_Used',
                'Total_PGA_Allocated',
                'Total_PGA_Used_by_SQL_Workareas'
            ]:
                self.ciient.metric('oracle_sysmetric',
                                   {
                                       'metric_value': random.uniform(0.0, 7.0),
                                   },
                                   tags=merge(common_tags, {"metric_name": metric_name}),

                                   )

    def call_function(self, name, count):
        if name in self.loopup_dict.keys():
            if getattr(self, self.loopup_dict[name], None):
                getattr(self, self.loopup_dict[name])(count)


if __name__ == "__main__":
    # Parse command line arguments
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-t", "--type", default="cpu",
                        help="type of the metric [cpu | memory]")
    parser.add_argument("-n", "--name", default="apache",
                        help="type of the metric [apache | iisserver | oracle | tomcat | sqlserver]")
    parser.add_argument("-c", "--count", default=100, type=int, help="metric count to send")
    parser.add_argument("-s", "--sleep", default=10, type=int,
                        help="sleep suration betwwen seding metric in seconds (like 10 or 60  (1 min) or 300 (5 mins)")
    parser.add_argument("-i", "--iteration", default=60, type=int,
                        help="Nunmber of times metric to be sent")
    parser.add_argument("-a", "--host_port", default='127.0.0.1:8092', help='host_ip:port')
    args = vars(parser.parse_args())
    host, port = args['host_port'].split(':')
    print(f"host={host} port={port}")
    if args['iteration'] <= 0: args['iteration'] = 1
    if args['count'] <= 0: args['count'] = 1
    if args['sleep'] < 10:
        print(f"Setting to default sleep duration 10 seconds betwwen sendfing the metrics")
        args['iteration'] = 10

    tsender = TelegraphSender(host=host, port=int(port))
    if f"{args['name'].lower()}_{args['type'].lower()}" in tsender.loopup_dict.keys():
        time.sleep(random.uniform(1.0, 5.0))
        for i in range(args['iteration']):
            print(f"Iteration={i + 1}: sending {args['name']} {args['type']} metrics....")
            tsender.call_function(f"{args['name'].lower()}_{args['type'].lower()}", args['count'])
            print(f"sleeping for {args['sleep']} seconds..")
            time.sleep(args['sleep'])
    else:
        print(f"Unable to find metric generetor {args['name']}")
