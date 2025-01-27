import pandas as pd
from typing import List, Callable

from llmint.assemble.pandas.transform import (
    add, copy, default, missing, apply, scale, shift
)
from llmint.map.function import Map


def assemble(mappings: list[Map]):
    output = []
    
    for mapping in mappings:
        match mapping.transformation.split(' ')[0]:
            case 'ADD':
                output.append(add(mapping))
            case 'COPY':
                output.append(copy(mapping))
            case 'DEFAULT':
                output.append(default(mapping))
            case 'MISSING':
                output.append(missing(mapping))
            case 'APPLY':
                output.append(apply(mapping))
            case 'SCALE':
                output.append(scale(mapping))
            case 'SHIFT':
                output.append(shift(mapping))   
                
    return output


def construct(df: pd.DataFrame, assembly: List[Callable[[pd.DataFrame], pd.Series]]):
    df_output = []
    
    for func in assembly:
        df_output.append(func(df))
    
    return pd.concat(df_output, axis=1)
