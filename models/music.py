class Music():
    
    def __init__(self, dyn_resource):
        self.dyn_resource = dyn_resource
        self.table = self.dyn_resource.Table('Music')