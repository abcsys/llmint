import re
from pandas import Series, DataFrame

from llmint.map.function import Map


def func(mapping: Map):
    apply_func = re.search(r'APPLY (.*)', mapping.transformation).group(1)
    
    def apply(df: DataFrame):
        # assign all columns to their own variables
        for col in df.columns:
            exec(f'{col.replace(" ", "_")} = df[col]', locals(), globals())

        exec(f'_output = {apply_func}', locals(), globals())
        
        return Series(_output, name=mapping.target_field)
    
    return apply
