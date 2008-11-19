from graph import GraphModel
from yamlserializer import SaveModel,LoadModel

if __name__ == "__main__":
    print "run test"
    graphmodel = GraphModel()
    newnode = graphmodel.new("GraphNodeModel")
    # subscribe
    class myevh(object):
        def propertychange(self,name,value):
            print " *- propertychanged!",name,value
        def addchild(self,child):
            print " *- addchild",child
        def delchild(self,child):
            print " *- delchild",child
    graphmodel.subscribe(myevh())
    newnode.subscribe(myevh())
    # change property
    newnode.setProperty("name","bla")
    # add/remove node to graph
    graphmodel.addChild(newnode)
    graphmodel.delChild(newnode)
    graphmodel.addChild(newnode)
    # add/remove connectors to graph
    newconnector = graphmodel.new("GraphNodeConnectorModel")
    newconnector.subscribe(myevh())
    newconnector.setProperty("name","bla")
    assert newconnector.getProperty("name") == "bla"
    #assert newconnector.name == "bla" # XXX no magic for the moment
    newnode.addChild(newconnector)
    newnode.delChild(newconnector)
    newnode.addChild(newconnector)
    # create connections
    newnode2 = graphmodel.new("GraphNodeModel")
    newconnector2 = graphmodel.new("GraphNodeConnectorModel")
    newnode2.addChild(newconnector2)
    newconnection = graphmodel.new("GraphConnectionModel",newconnector,newconnector2)
    graphmodel.addChild(newconnection)
    graphmodel.delChild(newconnection)
    graphmodel.addChild(newconnection)
    newnode.addChild(newnode2)

    print " * model --> save --> data"
    data = SaveModel(graphmodel)
    #print data
    print " * data --> load --> model2"
    graphmodel2 = LoadModel(data,"GraphModel")
    print " * model2 --> save --> data2"
    data2 = SaveModel(graphmodel2[0])
    #print data2
    print " * assert data == data2"
    assert data == data2

    print data
