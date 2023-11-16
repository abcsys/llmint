def addFunction(target_field, field_type):
    return f'{{ from: , to: {target_field}, transformation: ADD {target_field} TYPE {field_type} }}'   