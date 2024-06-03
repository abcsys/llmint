from llmint.core import util

from llmint.core import model

def map(source_schema,
        target_schema,
        include_reasoning=False,
        include_info=False):
    messages = []
    util.get_system_prompt(messages)
    util.get_user_prompt(messages, source_schema, target_schema)

    # remove reasoning from output
    # XXX
    response_info = model.call(messages)
    if not include_reasoning:
        for i in range(len(response_info[0])):
            response_info[0][i] = response_info[0][i][0]

    if include_info:
        return response_info
    return response_info[0]


def route(name, args):
    match name:
        case "copy":
            return copy(source_field=args.get("source_field"),
                        target_field=args.get("target_field"),
                        reasoning=args.get("reasoning"))
        case "addOptionalFunction":
            return addOptionalFunction(target_field=args.get("target_field"),
                                       field_type=args.get("field_type"),
                                       reasoning=args.get("reasoning"))
        case "castFunction":
            return castFunction(source_field=args.get("source_field"),
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
        case "incompatibleFunction":
            return incompatibleFunction(reasoning=args.get("reasoning"))
        case "sendMessageFunction":
            return sendMessageFunction(message=args.get("message"))
