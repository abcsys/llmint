import pandas as pd

from llmint.assemble.pandas.transform import (
    add, cast, copy, default, delete, missing, rename, apply, link, scale, shift
)
from llmint.map.function import Map

def assemble(df: pd.DataFrame, mappings: list[Map]):
    df_outputs = []
    
    for mapping in mappings:
        match mapping.transformation.split(' ')[0]:
            case 'ADD':
                df_outputs.append(add(df, mapping))
            case 'CAST':
                df_outputs.append(cast(df, mapping))
            case 'COPY':
                df_outputs.append(copy(df, mapping))
            case 'DEFAULT':
                df_outputs.append(default(df, mapping))
            case 'DELETE':
                df_outputs.append(delete(df, mapping))
            case 'MISSING':
                df_outputs.append(missing(df, mapping))
            case 'RENAME':
                df_outputs.append(rename(df, mapping))
            case 'APPLY':
                df_outputs.append(apply(df, mapping))
            case 'LINK':
                df_outputs.append(link(df, mapping))
            case 'SCALE':
                df_outputs.append(scale(df, mapping))
            case 'SHIFT':
                df_outputs.append(shift(df, mapping))   
                
    return pd.concat(df_outputs, axis=1)
