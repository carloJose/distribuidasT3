from metaSingleton import MetaSingleton

class Storage(metaclass=MetaSingleton):

    def __init__(self):
        self.data = []

    def add_node_info(self,info):
        self.data.append(info)
    
    def get_data_by_index(self,index):
        return self.data[index]