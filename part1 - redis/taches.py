import json, requests, os, sys;

class T1:
    def __init__(self, params):
    #params is a dictionary that contains all variables and
    #parameters needed to execute the task. In particular
    #params contains all input values to the task
        print("T1 init")
        self.data = None
        self.params = params
    
    def extract(self):
        print("T1 extract")
        with open(os.path.join(sys.path[0], self.params["path"])) as f:
            self.data = json.load(f)
    
    def load(self):
        print("T1 load")
        return self.data

class T2:
    def __init__(self, params):
    #params is a dictionary that contains all variables and
    #parameters needed to execute the task. In particular
    #params contains all input values to the task
        print("T2 init")
        self.data = None;
        self.params = params;
    
    def extract(self):
        print("T2 extract")
        with open(os.path.join(sys.path[0], self.params["path"])) as f:
            self.data = json.load(f)
    
    def load(self):
        print("T2 load")
        return {"task": "T3", "params": {"apis": json.dumps(self.data)}}
        
class T3:
    def __init__(self, params):
    #params is a dictionary that contains all variables and
    #parameters needed to execute the task. In particular
    #params contains all input values to the task
        print("T3 init")
        self.data = None
        self.params = params
    
    def extract(self):
        print("T3 extract")
        apis = json.loads(self.params["apis"])
        response = requests.get(apis["ip"])
        self.data = response.json()
    
    def load(self):
        print("T3 load")
        return self.data