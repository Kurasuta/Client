class Plugin:
    _version="0.1"
    _name="test"

    def register(self):
        return self._name, self._version
        
    def acquire(self, job):
        path = ''
        return path