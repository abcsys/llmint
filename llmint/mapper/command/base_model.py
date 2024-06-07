import time
from openai import OpenAI
import llmint.mapper.command.util as util

def call(source_schema, target_schema):
    client = OpenAI(api_key=util.get_openai_api_key())
    
    start_time = time.time()
    response = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "Generate schema evolution mappings that can translate from the source database schema to the target database schema. "},
            {"role": "user", "content": "Source Schema: {} Target Schema: {}".format(source_schema, target_schema)}
        ]
    )
    response_time = round(time.time() - start_time, 3)
    print(f"Generating response took {response_time} seconds")
    
    print("Token Usage: ", response.usage, flush=True)
    print(response.choices[0].message.content.encode("utf-8"))
    return response, response.usage.total_tokens, response_time