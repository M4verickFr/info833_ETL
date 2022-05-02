import taches, redis, string, random;

def generate_random_hash():
    return "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))

r = redis.Redis(host='localhost', port=6379, db=0, charset="utf-8")
r.delete("task_queue")

params = {"path": "data-T1.json"}
# Generate random hash
hash = generate_random_hash()
r.hset(hash, mapping=params)
r.rpush("task_queue", f"T1:{hash}")

while (r.llen("task_queue") > 0):
    task = (r.lpop("task_queue")).decode("utf-8")
    taskName = task.split(":")[0]
    hash = task.split(":")[1]
    params = r.hgetall(hash)
    r.delete(hash)
    params = {k.decode("utf-8"): v.decode("utf-8") for k, v in params.items()}
    
    taskObject = getattr(taches, taskName)(params)
    taskObject.extract()
    data = taskObject.load()
    
    if ("task" in data):
        hash = generate_random_hash()
        params = data["params"] or {}
        r.hset(hash, mapping=params)
        r.rpush("task_queue", data["task"] + ":" + hash)
    else:
        print(data)