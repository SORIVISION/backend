import os
from openai import OpenAI

async def get_gpt_response(sys_prompt, user_prompt, image_url) :
    client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

    messages =[
        {"role" : "system", "content" : sys_prompt},
        {"role" : "user", "content" : [{"type" : "text", "text" : user_prompt }, 
                                       {"type" : "image_url" , "image_url" : {"url" : image_url}}]}
    ]
    response = client.chat.completions.create(
        model = os.getenv("OPENAI_API_MODEL_NAME"),
        messages = messages,
        max_tokens = os.getenv("OPENAI_API_MAX_TOKENS"),
        temperature = os.getenv("OPENAI_API_TEMPERATURE")
    )

    return response.choices[0].message.content