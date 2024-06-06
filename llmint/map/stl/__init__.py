# TBD check if command routing is necessary
# from llmint.map.stl import (
#     schema,
#     field,
#     value,
# )
#
#
# def command_route(name, args):
#     match name:
#         # schema matching
#         case "match":
#             return schema.match.func(
#                 source_schema=args.get("source_schema"),
#                 target_schema=args.get("target_schema"),
#             )
#         # field transformation
#         case "add":
#             return field.add.func(
#                 target_field=args.get("target_field"),
#                 field_type=args.get("field_type"),
#                 reasoning=args.get("reasoning")
#             )
#         case "cast":
#             return field.cast.func(
#                 source_field=args.get("source_field"),
#                 target_field=args.get("target_field"),
#                 source_type=args.get("source_type"),
#                 target_type=args.get("target_type"),
#                 reasoning=args.get("reasoning")
#             )
#         case "copy":
#             return field.copy.func(
#                 source_field=args.get("source_field"),
#                 target_field=args.get("target_field"),
#                 reasoning=args.get("reasoning")
#             )
#         case "default":
#             return field.default.func(
#                 source_field=args.get("source_field"),
#                 target_field=args.get("target_field"),
#                 default_value=args.get("default_value"),
#                 reasoning=args.get("reasoning")
#             )
#         case "delete":
#             return field.delete.func(
#                 source_field=args.get("source_field"),
#                 reasoning=args.get("reasoning")
#             )
#         case "rename":
#             return field.rename.func(
#                 source_field=args.get("source_field"),
#                 target_field=args.get("target_field"),
#                 reasoning=args.get("reasoning")
#             )
#         case "missing":
#             return field.missing.func(
#                 target_field=args.get("target_field"),
#                 reasoning=args.get("reasoning")
#             )
#         # value transformation
#         case "link":
#             return value.link.func(
#                 source_field=args.get("source_field"),
#                 target_field=args.get("target_field"),
#                 old_value=args.get("old_value"),
#                 new_value=args.get("new_value"),
#                 reasoning=args.get("reasoning")
#             )
#         case "scale":
#             return value.scale.func(
#                 source_field=args.get("source_field"),
#                 target_field=args.get("target_field"),
#                 factor=args.get("factor"),
#                 reasoning=args.get("reasoning")
#             )
#         case "shift":
#             return value.shift.func(
#                 source_field=args.get("source_field"),
#                 target_field=args.get("target_field"),
#                 value=args.get("value"),
#                 reasoning=args.get("reasoning")
#             )
#         case "gen":
#             return value.gen.func(
#                 source_field=args.get("source_field"),
#                 target_field=args.get("target_field"),
#                 conversion_equation=args.get("conversion_equation"),
#                 reasoning=args.get("reasoning")
#             )
#         case "apply":
#             return value.apply.func(
#                 source_field=args.get("source_field"),
#                 target_field=args.get("target_field"),
#                 function_name=args.get("function_name"),
#                 reasoning=args.get("reasoning")
#             )
