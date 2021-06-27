from metaSingleton import MetaSingleton
from storage import Storage as stg

class Watch(metaclass=MetaSingleton):
    
    # calsse relogio vetorial
    def __init__(self):
        self.watch = None