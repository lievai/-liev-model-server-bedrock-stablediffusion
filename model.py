import json
from flask import Flask, request, send_file
from flask_httpauth import HTTPBasicAuth
from flask_restful import Api
from dotenv import load_dotenv
import base64
import io
import json
import logging

# External Dependencies:
import boto3
from PIL import Image
import os, io

from config.config import Config

load_dotenv()
config = Config('bedrock-stablediffusion')

LIEV_PASSWORD          = config.get("LIEV_PASSWORD")
LIEV_USERNAME          = config.get("LIEV_USERNAME")

# Initialize logging to console - do not use file appenders in container mode
logging.basicConfig(level=config.get('LOG_LEVEL', default= 'INFO'), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()

@auth.verify_password
def verify(username, password):
    """ Verify: Check username and password to allow access to the API"""
    if not (username and password):
        return False
    return username == LIEV_USERNAME and password == LIEV_PASSWORD

@app.route('/image')
@auth.login_required
def image():
    # Init Bedrock Client
    AWS_ACCESS_KEY_ID      = config.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY  = config.get("AWS_SECRET_ACCESS_KEY")
    AWS_REGION_NAME        = config.get("AWS_REGION_NAME")
    BEDROCK_MODELID        = config.get("BEDROCK_MODELID")


    boto_session = boto3.Session(aws_access_key_id     = AWS_ACCESS_KEY_ID,
                                aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
                                region_name           = AWS_REGION_NAME)

    bedrock_runtime = boto_session.client(service_name='bedrock-runtime')



    data = request.data
    try:
        data = json.loads(data)
    except:
        return json.dumps("JSON load problem !"), 500

    if isinstance(data, dict) == False:
        return json.dumps("JSON load conversion problem. Not a dict ! Are you using data payload  ?"), 500

    instruction     = data.get('instruction', "a smiley woman")
    negative_prompt = data.get('negative_prompt', "")
    cfg_scale       = data.get('cfg_scale', 10)
    steps           = data.get('steps', 50)
    width           = data.get('width', 512)
    height          = data.get('height', 512)
    seed            = data.get('seed', None)
    style_preset    = data.get('style_preset', None)

    # 20231209 - Cleber
    # Need to make it better
    if seed:
        if style_preset:
            body = json.dumps(
                {
                    "text_prompts": (
                        [
                            {
                                "text": instruction,
                                "weight": 1
                            },
                            {
                                "text": negative_prompt,
                                "weight": -1
                            }
                        ]
                    ),
                    "cfg_scale" : cfg_scale,
                    "seed"      : seed,
                    "steps"     : steps,
                    "width"     : width,
                    "height"    : height,
                    "style_preset" : style_preset
                }
            )
        else:
            body = json.dumps(
                {
                    "text_prompts": (
                        [
                            {
                                "text": instruction,
                                "weight": 1
                            },
                            {
                                "text": negative_prompt,
                                "weight": -1
                            }
                        ]
                    ),
                    "cfg_scale" : cfg_scale,
                    "seed"      : seed,
                    "steps"     : steps,
                    "width"     : width,
                    "height"    : height
                }
            )            
    else:
        if style_preset:
            body = json.dumps(
                {
                    "text_prompts": (
                        [
                            {
                                "text"   : instruction,
                                "weight" : 1
                            },
                            {
                                "text"   : negative_prompt,
                                "weight" : -1
                            }
                        ]
                    ),
                    "cfg_scale" : cfg_scale,
                    "steps"     : steps,
                    "width"     : width,
                    "height"    : height,
                    "style_preset" : style_preset
                }
            )
        else:
            body = json.dumps(
                {
                    "text_prompts": (
                        [
                            {
                                "text"   : instruction,
                                "weight" : 1
                            },
                            {
                                "text"   : negative_prompt,
                                "weight" : -1
                            }
                        ]
                    ),
                    "cfg_scale" : cfg_scale,
                    "steps"     : steps,
                    "width"     : width,
                    "height"    : height
                }
            )            

    accept = "application/json"
    contentType = "application/json"
    
    try:
        response = bedrock_runtime.invoke_model(
            body=body, modelId=BEDROCK_MODELID, accept=accept, contentType=contentType
        )
        response_body = json.loads(response.get("body").read())
        base_64_img_str = response_body["artifacts"][0].get("base64")
        image = io.BytesIO(base64.decodebytes(bytes(base_64_img_str, "utf-8")))
        return send_file(image, mimetype='image/png'), 200
    except Exception as e:
        logger.error(e, exc_info=True)
        return None, 500

@app.route('/healthz')
def liveness():
    # You can add custom logic here to check the application's liveness
    # For simplicity, we'll just return a 200 OK response.
    return json.dumps({'status': 'OK'})

# Health check endpoint for readiness probe
@app.route('/readyz')
def readiness():
    # You can add custom logic here to check the application's readiness
    # For simplicity, we'll just return a 200 OK response.
    return json.dumps({'status': 'OK'})

#if __name__ == '__main__':
#    app.run(debug=False, port=5000, host='0.0.0.0')
