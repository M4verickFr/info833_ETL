import redis

r = redis.Redis(host='localhost', port=6379, db=0)
r.set('info833', 'ETL')
print(r.get('info833'))