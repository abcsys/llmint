# Field Transformation Tools
def addFunction(target_field, field_type):
    return f'{{from: None, to: {target_field}, transformation: ADD {target_field} TYPE {field_type}}}'   

def changeTypeFunction(source_field, target_field, source_type, target_type):
    return f'{{from: {source_field}, to: {target_field}, transformation: CHANGE TYPE {target_field} TO {target_type}}}'   

def deleteFunction(source_field):
    return f'{{from: {source_field}, to: None, transformation: DELETE {source_field}}}'

def renameFunction(source_field, target_field):
    return f'{{from: {source_field}, to: {target_field}, transformation: RENAME {source_field} TO {target_field}}}'

def setDefaultFunction(source_field, target_field, default_value):
    return f'{{from: {source_field}, to: {target_field}, transformation: SET_DEFAULT {target_field} TO {default_value}}}'   

# Value Transformation Tools
def applyFuncFunction(field_name, function_name):
    return f'{{from: {field_name}, to: {field_name}, transformation: APPLY_FUNC {field_name} {function_name}}}'   

def mapFunction(field, old_value, new_value):
    return f'{{from: {field}, to: {field}, transformation: MAP {field} "{old_value}" TO "{new_value}"}}'   

def scaleFunction(field, factor):
    return f'{{from: {field}, to: {field}, transformation: SCALE {field} BY {factor}}}'   

def shiftFunction(field, value):
    return f'{{from: {field}, to: {field}, transformation: SHIFT {field} BY {value}}}'   

# Extended Command Tools
def combineFunction(field_1, field_2, new_field, operation):
     return f'{{from: ({field_1} {field_2}), to: new_field, transformation: COMBINE {field_1}, {field_2} TO {new_field} USING {operation}}}'   

def splitFunction(source_field, new_field_1, new_field_2, delimiter):
    return f'{{ from: {source_field}, to: ({new_field_1} {new_field_2}), transformation: SPLIT {source_field} INTO {new_field_1}, {new_field_2} BY {delimiter}}}'   
