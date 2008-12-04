import yaml

import dictserializer

def LoadModel(yamldata,reqclsname):
    objs = yaml.load(yamldata)
    return dictserializer.LoadModel(objs,reqclsname)

def SaveModel(model,data=""):
    # save children
    for child in model.getChildren():
         data = SaveModel(child,data)
    # to dict
    obj = dictserializer.SaveModel(model)
    # dump to yaml
    data += yaml.dump(obj)
    return data

