import pandas as pd

import llmint
from llmint.assemble.pandas import assemble, construct


def main():
    source_schema = '''
    {
        "fields": [
            {"name": "Fname", "type": "string"},
            {"name": "Lname", "type": "string"},
            {"name": "Age", "type": "int"},
            {"name": "Email", "type": ["null", "string"], "default": null}
        ]
    }
    '''
    target_schema = '''
    {
        "fields": [
            {"name": "name", "type": "string"},
            {"name": "age", "type": "int"},
            {"name": "email", "type": ["null", "string"], "default": null}
        ]
    }
    '''
    
    
    source_df = pd.DataFrame([{"Fname": "Josh", "Lname": "Doe", "Age": 31, "Email": "joshdoe@example.com"}])
    dest_df = pd.DataFrame([{"name": "Jane Doe", "age": 27, "email": "janedoe@example.com"}])
    print("Concat the source dataframe to the dest dataframe:")
    print("Source:", source_df, sep="\n")
    print("Dest:", dest_df, sep="\n")

    mappings = llmint.map(source_schema, target_schema)
    assembly = assemble(mappings)
    output = construct(source_df, assembly)
    
    combined_df = pd.concat([dest_df, output], axis=0)
    print("\nCombined:", combined_df, sep="\n")


if __name__ == "__main__":
    main()
