from multiprocessing import Process
import taches, redis, string, random, time;

r = redis.Redis(host='localhost', port=6379, db=0);

def generate_random_hash():
    return "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16));

def make_task(task):
    taskName = task.split(":")[0]
    hash = task.split(":")[1]
    params = r.hgetall(hash)
    r.delete(hash)
    params = {k.decode("utf-8"): v.decode("utf-8") for k, v in params.items()}
    
    taskObject = getattr(taches, taskName)(params)
    taskObject.extract();
    data = taskObject.load();
    
    if ("task" in data):
        hash = generate_random_hash()
        params = data["params"] or {}
        r.hset(hash, mapping=params)
        r.rpush("task_queue", data["task"] + ":" + hash)
    else:
        print(data)
    
def init():
    r.delete("task_queue");

    params = {"path": "data-T1.json"}
    # Generate random hash
    hash = generate_random_hash()
    r.hset(hash, mapping=params)
    r.rpush("task_queue", f"T1:{hash}")
    
    return r

def main():
    while(True):
        if (r.llen("task_queue") == 0):
            print("No tasks, waiting...")
            for i in range(0, 10): # wait 10s, test each 1s
                time.sleep(1) 
                if (r.llen("task_queue") > 0):
                    break;
            if (r.llen("task_queue") == 0):
                print("No tasks during 10s, exiting...")
                break;
    
        print("Tasks found, starting...")
        task = (r.lpop("task_queue")).decode("utf-8")
        p = Process(target=make_task, args=(task,))
        p.start()

if __name__ == '__main__':
    init()
    main()