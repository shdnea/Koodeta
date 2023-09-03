import hou

def getNodeName():
    try:
        for node in hou.selectedNodes():
            node_name = node
            return str(node_name)
    except:
        pass
    
def getNodePath():
    try:
        for node in hou.selectedNodes():
            node_path = node.path()
            return node_path
    except:
        pass