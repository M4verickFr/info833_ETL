from collections import Counter
from multiprocessing import Process
import redis, string, random, time, os, sys, math, json, re;

path = "./text.txt"
r = redis.StrictRedis('localhost', 6379, charset="utf-8", decode_responses=True)
nbProcessMax = 7

def getNbProcess(nbWords):
    nbProcess = math.ceil(math.log(nbWords))

    nbProcess = nbProcess if nbProcess > 0 else 1
    nbProcess = nbProcess if nbProcess <= nbProcessMax else nbProcessMax

    return nbProcess

def generate_random_hash():
    return "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))

def map(words):
    counts = dict()

    for word in words:
        word = re.sub('[^A-Za-z0-9]+', '', word)
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    if len(counts) > 0:
        hash = generate_random_hash()
        r.hset(hash, mapping=counts)
        r.publish('reduce', hash)

def reduce(hash1, hash2):
    counts1 = r.hgetall(hash1)
    r.delete(hash1)
    counts1 = {k: int(v) for k, v in counts1.items()}

    counts2 = r.hgetall(hash2)
    r.delete(hash2)
    counts2 = {k: int(v) for k, v in counts2.items()}

    counts = {k: counts1.get(k, 0) + counts2.get(k, 0) for k in set(counts1) | set(counts2)}

    hash = generate_random_hash()
    r.hset(hash, mapping=counts)
    r.publish('reduce', hash)

def finish(hash):
    counts = r.hgetall(hash)
    counts = {k: int(v) for k, v in counts.items()}
    counts = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))

    with open(os.path.join(sys.path[0], "result.json"), "w") as outfile:
        json.dump(counts, outfile, indent = 4)

    print("Results are available in result.json and in redis with: HGETALL {hash}")
    exit()

def main():
    file = open(os.path.join(sys.path[0], path), "rt")
    data = file.read()
    words = data.split()
    nbWords = len(words)
    nbProcess = getNbProcess(nbWords)
    nbReducerRunning = 0
    totalNumReduce = ((nbProcess - 1) if nbProcess > 1 else 1)
    print(nbProcess, totalNumReduce)

    for i in range(nbProcess):
        start = math.floor(nbWords/nbProcess*i)
        end = math.floor(nbWords/nbProcess*(i+1))
        print(f"Start map process from {start} to {end}")
        p = Process(target=map, args=(words[start:end],))
        p.start()

    tmpHash = None

    sub = r.pubsub()
    sub.subscribe('reduce')
    for message in sub.listen():
        if message is not None and isinstance(message, dict) and message.get('type') == "message":
            hash = message.get('data')
            if (nbReducerRunning == totalNumReduce):
                    finish(hash)
            elif tmpHash is None:
                print("Save hash to reduce with next message")
                tmpHash = hash
            else:
                print("Start reduce process")
                nbReducerRunning += 1
                p = Process(target=reduce, args=(hash, tmpHash))
                p.start()
                tmpHash = None

if __name__ == '__main__':
    main()