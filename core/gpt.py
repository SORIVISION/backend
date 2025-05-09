import os
from openai import OpenAI
import base64
import requests

def image_url_to_base64_data_url(image_url: str, mime_type: str = "image/png") -> str:
    response = requests.get(image_url)
    
    if response.status_code != 200:
        raise Exception(f"Failed to download image: {response.status_code}")
    
    base64_str = base64.b64encode(response.content).decode('utf-8')
    
    data_url = f"data:{mime_type};base64,{base64_str}"
    
    return data_url

async def get_gpt_response(sys_prompt, user_prompt, image_url) :
    client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

    image_data_url = image_url_to_base64_data_url(image_url)

    messages =[
        {"role" : "system", "content" : sys_prompt},
        {"role" : "user", "content" : [{"type" : "text", "text" : user_prompt }, 
                                {"type" : "image_url" , "image_url" : {"url" : image_data_url}}]}
    ]
    response = client.chat.completions.create(
        model = os.getenv("OPENAI_API_MODEL_NAME"),
        messages = messages,
        max_tokens = os.getenv("OPENAI_API_MAX_TOKENS"),
        temperature = os.getenv("OPENAI_API_TEMPERATURE")
    )

    return response.choices[0].message.content
