import redis
import sys
import time
import socket

import boundary_plugin

params = boundary_plugin.parse_params()
redis_server = params.get('redis_hostname', None) or 'localhost'
redis_port = int(params.get('redis_port', None) or 6379)
redis_password = params.get('redis_password', None) or None

if not redis_password:
    redis_password = None
r = redis.Redis(redis_server, redis_port, password=redis_password)

_accum = dict()

def accum(stat_name, new_value):
    global _accum

    try:
        old_value = _accum[stat_name]
    except KeyError:
        old_value = new_value

    diff = new_value - old_value
    _accum[stat_name] = new_value
    return diff

# List of values returned from Redis' info call to report to Boundary.
# Each value has a boolean specifying whether to aggregate data (i.e. report
# only delta from the previous value) or report the metric as-is.
values_to_report = (
    ('connected_clients', False),
    ('keyspace_hits', True),
    ('keyspace_misses', True),
    ('expired_keys', True),
    ('evicted_keys', True),
    ('total_commands_processed', True),
    ('total_connections_received', True),
    ('used_memory_rss', False),
)

while True:
    info = r.info()

    for v,aggregate in values_to_report:
        val = accum(v, info[v]) if aggregate else info[v]
        boundary_plugin.boundary_report_metric('REDISX_' + v.upper(), val)

    boundary_plugin.sleep_interval()

