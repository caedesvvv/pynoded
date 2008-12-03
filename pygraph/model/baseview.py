"""
Base classes for a view structure.
"""

class ViewObjectBase(object):
    """
    Base class for a view object.

    Subscribes to the model, keeps some instance data, and notifies the
    ModelViewBase on changes to the graph.

    Subclasses are usually responsible for holding an instance representation in the view,
    owning the view engine specific object if necessary, and answering to model callbacks
    to update properties or modify parenting.
    """
    def __init__(self,view,parent,model):
        model.subscribe(self)
        self._view = view
        self._parent = parent
        self._model = model
        self._instance = None

    # model callbacks
    def addchild(self, child):
        self._view.traverse(self._model,child)

    def delchild(self, child):
        self._view.removeBranch(self._model,child)


class ModelViewBase(object):
    """
    Base class an engine view.

    Handles logic for traversing and recreating a model into the view.
    Creates view classes for the model based on the instance dict: _model2view.

    Subclasses are responsible for declaring their class mappings, and holding
    common data for the engine (all children get a pointer to the view).
    """
    def __init__(self,model):
        self._model = model
        self._instances = {}
        self.traverse(None,model)
        model.subscribe(self)

    def removeBranch(self,parent,model):
        if model in self._instances:
            for child in model.getChildren():
                self.removeBranch(model,child)
            del self._instances[model]

    def traverse(self,parent,model):
        self.process(parent,model)
        for child in model.getChildren():
            self.traverse(model,child)

    def process(self,parent,model):
        class_name = model.__class__.__name__
        if not class_name in self._model2view:
            return
        for klass in self._model2view[class_name]:
            inst = klass(self,parent,model)
            self._instances[model.uuid] = inst

    # model callbacks
    def addchild(self,child):
        self.traverse(self._model,child)

    def delchild(self,child):
        self.removeBranch(self._model,child)

