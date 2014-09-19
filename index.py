import redis
import sys
import time
import socket

if not 1 <= len(sys.argv) <= 5:
    print "Usage: %s [redis_server] [redis_port] [poll_interval] [redis_password]" % sys.argv[0]
    print "[redis_server] is the server to connect to (the default is 'localhost')"
    print "[redis_port] is the TCP port to connect to (the default is 6379)"
    print "[poll_interval] is the interval, in milliseconds, at which we display statistics; default is 1000"
    print "[redis_password] is the password to use to authenticate with Redis (default is none)"
    sys.exit(-1)

redis_server = sys.argv[1] if len(sys.argv) >= 2 else 'localhost'
redis_port = int(sys.argv[2]) if len(sys.argv) >= 3 else 6379
poll_interval = int(sys.argv[3]) if len(sys.argv) >= 4 else 1000
redis_password = sys.argv[4] if len(sys.argv) >= 5 else None

hostname = socket.gethostname()

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
        print "%s %d %s" % ('REDIS_' + v.upper(), accum(v, info[v]), hostname)

    time.sleep(float(poll_interval) / 1000)

