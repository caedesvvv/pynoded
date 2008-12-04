# choose one of the following two
from metamodel.basemodel import SubscribableModel
#from dmvcmodel import DMVCSubscribableModel as SubscribableModel

########################################################
# graph interface

class GraphModel(SubscribableModel):
    def __init__(self):
        SubscribableModel.__init__(self)

class GraphNodeModel(SubscribableModel):
    def __init__(self):
        SubscribableModel.__init__(self)

class GraphNodeConnectorModel(SubscribableModel):
    def __init__(self):
        SubscribableModel.__init__(self)

class GraphConnectionModel(SubscribableModel):
    def __init__(self,origin=None,destination=None):
        SubscribableModel.__init__(self)
        self.setProperty("origin",origin)
        self.setProperty("destination",destination)


