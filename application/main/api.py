import base64
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from starlette.responses import PlainTextResponse, JSONResponse
from application.llm.llm_runner_industry_sector import llm_industry_sector_cross_tabulation as ctis_llm
from application.llm.llm_runner_industry_sector import llm_industry_hs_codes_cross_tabulation as ctihs_llm
from application.llm.llm_runner_industry_sector import llm_industry_sector_dendogram as dis_llm
from application.llm.llm_runner_industry_sector import llm_industry_product_dendogram as dip_llm
from application.llm.llm_runner_showroom import llm_showroom_histogram as hs_llm
from application.llm.llm_runner_showroom import llm_showroom_kde as ks_llm
from application.llm.llm_runner_warehouse import llm_warehouse_histogram_cbm as hs_cbm_llm
from application.llm.llm_runner_warehouse import llm_warehouse_histogram_mt as hs_mt_llm
from application.llm.llm_runner_warehouse import llm_warehouse_kde_cbm as ks_cbm_llm
from application.llm.llm_runner_warehouse import llm_warehouse_kde_mt as ks_mt_llm
from application.llm.llm_runner_willingness_to_pay import llm_willingness_scatterplot as spw_llm
from application.llm.llm_runner_willingness_to_pay import llm_willingness_boxplot as bpw_llm
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

@app.get('/industry_cluster_sector_analysis_cross_tab', status_code=200)
def get_industry_sector_analysis_cross_tab():
    output, buf = ctis_llm()
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode('ascii')
    api_output = JSONResponse(
        {
            'llm_output': output,
            'img': img_b64
        }
    )
    return api_output

@app.get('/industry_cluster_product_analysis_cross_tab', status_code=200)
def get_industry_product_analysis_cross_tab():
    output, buf = ctihs_llm()
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode('ascii')
    api_output = JSONResponse(
        {
            'llm_output': output,
            'img': img_b64
        }
    )
    return api_output

@app.get('/industry_cluster_sector_analysis_dendogram', status_code=200)
def get_industry_sector_analysis_dendogram():
    output, buf = dis_llm()
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode('ascii')
    api_output = JSONResponse(
        {
            'llm_output': output,
            'img': img_b64
        }
    )
    return api_output

@app.get('/industry_cluster_product_analysis_dendogram', status_code=200)
def get_industry_product_analysis_dendogram():
    output, buf = dip_llm()
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode('ascii')
    api_output = JSONResponse(
        {
            'llm_output': output,
            'img': img_b64
        }
    )
    return api_output

@app.get('/showroom_size_analysis_histogram', status_code=200)
def get_showroom_size_analysis_histogram():
    output, buf = hs_llm()
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode('ascii')
    api_output = JSONResponse(
        {
            'llm_output': output,
            'img': img_b64
        }
    )
    return api_output

@app.get('/showroom_size_analysis_kde', status_code=200)
def get_showroom_size_analysis_kde():
    output, buf = ks_llm()
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode('ascii')
    api_output = JSONResponse(
        {
            'llm_output': output,
            'img': img_b64
        }
    )
    return api_output

@app.get('/warehouse_size_analysis_histogram_cbm', status_code=200)
def get_warehouse_size_analysis_histogram_cbm():
    output, buf = hs_cbm_llm()
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode('ascii')
    api_output = JSONResponse(
        {
            'llm_output': output,
            'img': img_b64
        }
    )
    return api_output

@app.get('/warehouse_size_analysis_histogram_mt', status_code=200)
def get_warehouse_size_analysis_histogram_mt():
    output, buf = hs_mt_llm()
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode('ascii')
    api_output = JSONResponse(
        {
            'llm_output': output,
            'img': img_b64
        }
    )
    return api_output

@app.get('/warehouse_size_analysis_kde_cbm', status_code=200)
def get_warehouse_size_analysis_kde_cbm():
    output, buf = ks_cbm_llm()
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode('ascii')
    api_output = JSONResponse(
        {
            'llm_output': output,
            'img': img_b64
        }
    )
    return api_output

@app.get('/warehouse_size_analysis_kde_mt', status_code=200)
def get_warehouse_size_analysis_kde_mt():
    output, buf = ks_mt_llm()
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode('ascii')
    api_output = JSONResponse(
        {
            'llm_output': output,
            'img': img_b64
        }
    )
    return api_output

@app.get('/willingness_to_pay_analysis_scatter_plot', status_code=200)
def get_willingness_to_pay_analysis_scatter_plot():
    output, buf = spw_llm()
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode('ascii')
    api_output = JSONResponse(
        {
            'llm_output': output,
            'img': img_b64
        }
    )
    return api_output

@app.get('/willingness_to_pay_analysis_box_plot', status_code=200)
def get_willingness_to_pay_analysis_box_plot():
    output, buf = bpw_llm()
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode('ascii')
    api_output = JSONResponse(
        {
            'llm_output': output,
            'img': img_b64
        }
    )
    return api_output

# The following code snippet is just to test the API on local machine. Will not be needed when published.
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=int(os.getenv('PORT', 8000))) # 0.0.0.0 - for cloud deployments. For local deployment, use 127.0.0.1