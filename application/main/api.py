import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from starlette.responses import PlainTextResponse

from application.database import database as db

load_dotenv()
app = FastAPI(title='Questionnaire_DB API')

# CORS (Cross-Origin Resource Sharing) configuration - this allows external applications and websites to access this API
raw = os.getenv('ALLOWED_ORIGINS', '*') # This is the allowed list of websites that can access this API. '*' means anyone can access.
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
    allow_credentials=False
)

@app.post('/questionnaire', status_code=201)
def create_questionnaire(payload: dict):
    db.insert_into_questionnaire(payload)
    return {'status':'ok'}

@app.get('/hs_codes', status_code=200)
def get_hs_codes():
    return db.select_from_hs_codes_db()

@app.get('/questionnaire_fetch', status_code=200)
def get_questionnaire_db():
    return db.select_from_questionnaire_db()

@app.get('/healthz', status_code=200)
def get_healthz():
    return PlainTextResponse('ok')

# The following code snippet is just to test the API on local machine. Will not be needed when published.
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=int(os.getenv('PORT', 8000))) # 0.0.0.0 - for cloud deployments. For local deployment, use 127.0.0.1