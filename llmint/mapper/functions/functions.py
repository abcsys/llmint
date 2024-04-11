# ------------------------------------------------------------------------
# Field Transformation Tools
# ------------------------------------------------------------------------
def doNothingFunction(source_field, target_field, reasoning):
    return (f'{{from: {source_field}, to: {target_field}, transformation: DO NOTHING}}', reasoning)   

def addOptionalFunction(target_field, field_type, reasoning):
    return (f'{{from: None, to: {target_field}, transformation: ADD {target_field} TYPE {field_type}}}', reasoning)   

def changeTypeFunction(source_field, target_field, source_type, target_type, reasoning):
    return (f'{{from: {source_field}, to: {target_field}, transformation: CHANGE TYPE {source_field} FROM {source_type} TO {target_type}}}', reasoning)

def deleteFunction(source_field, reasoning):
    return (f'{{from: {source_field}, to: None, transformation: DELETE {source_field}}}', reasoning)

def renameFunction(source_field, target_field, reasoning):
    return (f'{{from: {source_field}, to: {target_field}, transformation: RENAME {source_field} TO {target_field}}}', reasoning)

def setDefaultFunction(source_field, target_field, default_value, reasoning):
    return (f'{{from: {source_field}, to: {target_field}, transformation: SET_DEFAULT {target_field} TO {default_value}}}', reasoning)

# ------------------------------------------------------------------------
# Value Transformation Tools
# ------------------------------------------------------------------------

def applyFuncFunction(source_field, target_field, function_name, reasoning):
    return (f'{{from: {source_field}, to: {target_field}, transformation: APPLY_FUNC {source_field} {function_name}}}', reasoning) 

def mapFunction(source_field, target_field, old_value, new_value, reasoning):
    return (f'{{from: {source_field}, to: {target_field}, transformation: MAP {source_field} "{old_value}" TO "{new_value}"}}', reasoning)

def scaleFunction(source_field, target_field, factor, reasoning):
    return (f'{{from: {source_field}, to: {target_field}, transformation: SCALE {source_field} BY {factor}}}', reasoning)   

def shiftFunction(source_field, target_field, value, reasoning):
    return (f'{{from: {source_field}, to: {target_field}, transformation: SHIFT {source_field} BY {value}}}', reasoning)   

# ------------------------------------------------------------------------
# Extended Command Tools
# ------------------------------------------------------------------------
def combineFunction(field_1, field_2, new_field, operation, reasoning):
     return (f'{{from: ({field_1}, {field_2}), to: {new_field}, transformation: COMBINE {field_1}, {field_2} TO {new_field} USING {operation}}}', reasoning)

def splitFunction(source_field, new_field_1, new_field_2, reasoning, delimiter=None):
    return (f'{{from: {source_field}, to: ({new_field_1}, {new_field_2}), transformation: SPLIT {source_field} INTO {new_field_1}, {new_field_2} BY {delimiter}}}', reasoning) 

def missingFunction(target_field, reasoning):
    return (f'{{from: None, to: {target_field}, transformation: MISSING {target_field}}}', reasoning)

def complexConversionFunction(source_field, target_field, conversion_equation, reasoning):
    return (f'{{from: {source_field}, to: {target_field}, transformation: CONVERT {conversion_equation}}}', reasoning)

def sendMessageFunction(message):
    return (message, "No reasoning")










def call_fn(name, args):
    match name:
        case "doNothingFunction":
            return doNothingFunction(source_field=args.get("source_field"), 
                                     target_field=args.get("target_field"), 
                                     reasoning=args.get("reasoning"))
        case "addOptionalFunction":
            return addOptionalFunction(target_field=args.get("target_field"), 
                                       field_type=args.get("field_type"),
                                       reasoning=args.get("reasoning"))
        case "changeTypeFunction":
            return changeTypeFunction(source_field=args.get("source_field"),
                                      target_field=args.get("target_field"),
                                      source_type=args.get("source_type"),
                                      target_type=args.get("target_type"),
                                      reasoning=args.get("reasoning"))
        case "deleteFunction":
            return deleteFunction(source_field=args.get("source_field"),
                                  reasoning=args.get("reasoning"))
        case "renameFunction":
            return renameFunction(source_field=args.get("source_field"),
                                  target_field=args.get("target_field"),
                                  reasoning=args.get("reasoning"))
        case "setDefaultFunction":
            return setDefaultFunction(source_field=args.get("source_field"),
                                      target_field=args.get("target_field"),
                                      default_value=args.get("default_value"),
                                      reasoning=args.get("reasoning"))
        case "applyFuncFunction":
            return applyFuncFunction(source_field=args.get("source_field"), 
                                     target_field=args.get("target_field"), 
                                     function_name=args.get("function_name"),
                                     reasoning=args.get("reasoning"))
        case "mapFunction":
            return mapFunction(source_field=args.get("source_field"), 
                               target_field=args.get("target_field"), 
                               old_value=args.get("old_value"),
                               new_value=args.get("new_value"),
                               reasoning=args.get("reasoning"))
        case "scaleFunction":
            return scaleFunction(source_field=args.get("source_field"), 
                                 target_field=args.get("target_field"), 
                                 factor=args.get("factor"),
                                 reasoning=args.get("reasoning"))
        case "shiftFunction":
            return shiftFunction(source_field=args.get("source_field"), 
                                 target_field=args.get("target_field"), 
                                 value=args.get("value"),
                                 reasoning=args.get("reasoning"))
        case "combineFunction":
            return combineFunction(field_1=args.get("field_1"),
                                   field_2=args.get("field_2"),
                                   new_field=args.get("new_field"),
                                   operation=args.get("operation"),
                                   reasoning=args.get("reasoning"))
        case "splitFunction":
            return splitFunction(source_field=args.get("source_field"),
                                 new_field_1=args.get("new_field_1"),
                                 new_field_2=args.get("new_field_2"),
                                 delimiter=args.get("delimiter"),
                                 reasoning=args.get("reasoning"))
        case "missingFunction":
            return missingFunction(target_field=args.get("target_field"),
                                   reasoning=args.get("reasoning"))
        case "complexConversionFunction":
            return complexConversionFunction(source_field=args.get("source_field"),
                                             target_field=args.get("target_field"),
                                             conversion_equation=args.get("conversion_equation"),
                                             reasoning=args.get("reasoning"))
        case "sendMessageFunction":
            return sendMessageFunction(message=args.get("message"))
                                     