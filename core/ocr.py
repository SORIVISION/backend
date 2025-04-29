import requests
import json
import os
import time

async def get_ocr(image_url) :
    """
    Input : image_url (string)
    Output : rescode, OCR text (string list) , RAW data
    (example)
    OCR text : ['반대쪽으로', '여십시오.', '영양정보', '총 내용량 500 ml' ...]
    RAW data : {'valueType': 'ALL', 
                'boundingPoly': {'vertices': [{'x': 103.0, 'y': 155.0},
                                            {'x': 170.0, 'y': 155.0}, 
                                            {'x': 170.0, 'y': 163.0}, 
                                            {'x': 103.0, 'y': 163.0}]}, 
                'inferText': '반대쪽으로', 
                'inferConfidence': 1.0, 
                'type': 'NORMAL', 
                'lineBreak': False}
    """

    url = os.getenv("CLOVA_OCR_URL")

    headers = {
        "X-OCR-SECRET": os.getenv("CLOVA_OCR_API_KEY"),
        "Content-Type": "application/json"
    }
    val = {
        'version' : 'V2',
        'requestId' : 'string',
        'timestamp' : str(int(time.time()) * 1000),
        'lang' : 'ko',
        'images' : [{'format' : 'png',
                     'name' : 'sorivision_ocr',
                     'url' : image_url}]
    }
    encoded_body = json.dumps(val).encode('UTF-8')
    response = requests.post(url, data=encoded_body, headers=headers)
    rescode = response.status_code
    content = json.loads(response.content.decode("UTF-8"))
    
    texts = []
    for f in content["images"][0]["fields"] :
        if ["inferConfidence"] > 0.6 :
            texts.append(f["inferText"])

    if(rescode == 200):
        return rescode, texts, content["images"][0]["fields"] # ocr result(text list) , raw data
    else:
        return rescode, None, None