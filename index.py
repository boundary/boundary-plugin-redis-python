import redis
import sys
import time
import socket

import boundary_plugin

params = boundary_plugin.parse_params()
redis_server = params.get('redis_hostname', 'localhost')
redis_port = int(params.get('redis_port', 6379))
redis_password = params.get('redis_password', None)

if not redis_password:
    redis_password = None
r = redis.Redis(redis_server, redis_port, password=redis_password)

_accum = dict()

def accum(stat_name, new_value):
    global _accum

    try:
        old_value = _accum[stat_name]
    except KeyError:
        _accum[stat_name] = new_value
        return new_value

    diff = new_value - old_value
    _accum[stat_name] = new_value
    return diff

values_to_report = (
    'connected_clients',
    'keyspace_hits',
    'keyspace_misses',
    'expired_keys',
    'evicted_keys',
    'total_commands_processed',
    'total_connections_received',
    'used_memory_rss',
)

while True:
    info = r.info()

    for v in values_to_report:
        boundary_plugin.boundary_report_metric('REDIS_' + v.upper(), accum(v, info[v]))

    boundary_plugin.sleep_interval()

