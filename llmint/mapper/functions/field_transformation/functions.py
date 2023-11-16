def addFunction(target_field, field_type):
    return f'{{ from: , to: {target_field}, transformation: ADD {target_field} TYPE {field_type} }}'   

def changeTypeFunction(source_field, target_field, source_type, target_type):
    return f'{{ from: {source_field}, to: {target_field}, transformation: CHANGE TYPE {target_field} TO {target_type} }}'   

def deleteFunction(source_field):
    return f'{{ from: {source_field}, to: , transformation: DELETE {source_field} }}'

def renameFunction(source_field, target_field):
    return f'{{ from: {source_field}, to: {target_field}, transformation: RENAME {source_field} TO {target_field} }}'

def setDefaultFunction(source_field, target_field, default_value):
    return f'{{ from: {source_field}, to: {target_field}, transformation: SET_DEFAULT {target_field} TYPE {default_value} }}'   