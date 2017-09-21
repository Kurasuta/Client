import os
import sys
import requests
import json

pluginpath = "Plugins/"

def load_plugins():
    plugins = {}
    # Load plugins
    sys.path.insert(0, pluginpath)
    for f in os.listdir(pluginpath):
        fname, ext = os.path.splitext(f)
        if ext == '.py':
            mod = __import__(fname)
            instance = mod.Plugin()
            try:
                name, version = instance.register()
                plugins[name] = {"version": version, "instance": instance}
                print("Loaded plugin %s successfully" % name)
            except AttributeError:
                print("Loading plugin %s failed" % fname)
    sys.path.pop(0)
    return plugins

def get_job(plugins):
    url = "http://127.0.0.1:5000"
    payload = {'plugins': plugins}
    head = {'Content-type':'application/json',
             'Accept':'application/json'}
    payld = json.dumps(payload)
    ret = requests.post(url,headers=head,data=payld)
    if ret.status_code == 200:
        return ret.json()
    else:
        return ret.status_code

def handle_job(plugins, job):
    print(job)
    
if __name__ == "__main__":
    plugins = load_plugins()
    job = get_job(list(plugins.keys()))
    handle_job(plugins, job)