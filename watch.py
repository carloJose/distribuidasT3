from metaSingleton import MetaSingleton
from storage import Storage as stg

class Watch(metaclass=MetaSingleton):
    
    def __init__(self):
        self.watch = None