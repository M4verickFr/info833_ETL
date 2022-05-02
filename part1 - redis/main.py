import taches;

# Traitement a effectuer
task_queue = []


objectT1 = taches.T1({"path": "data-T1.json"})
objectT1.extract()
dataT1 = objectT1.load()

task_queue.append({"task": dataT1["task"], "params": dataT1["params"]})

while (len(task_queue) > 0):
    task = task_queue.pop()
    taskObject = getattr(taches, task["task"])(task["params"])
    taskObject.extract();
    data = taskObject.load();
    
    if ("task" in data):
        task_queue.append({"task": data["task"], "params": data["params"] or None})
    else:
        print(data)