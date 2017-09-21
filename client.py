import os
import sys
import requests
import json
import importlib.util

pluginpath = "Plugins/"

def load_plugins():
    plugins = {}
    # Load plugins
    for d in os.listdir(pluginpath):
        possiblePlugin=os.path.join(pluginpath,d)
        if os.path.isdir(possiblePlugin):
            possiblePluginMain=os.path.join(possiblePlugin,"Plugin.py")
            if os.path.isfile(possiblePluginMain):
                spec = importlib.util.spec_from_file_location("Plugin", possiblePluginMain)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                instance = mod.Plugin()
                try:
                    name, version = instance.register()
                    plugins[name] = {"version": version, "instance": instance}
                    print("Loaded plugin %s successfully" % name)
                except AttributeError:
                    print("Loading plugin %s failed" % fname)
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
    #if len(plugins)>0:
    #    job = get_job(list(plugins.keys()))
    #    handle_job(plugins, job)