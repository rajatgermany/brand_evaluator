from app.api import api_v1_router
from app.core import config
from app.core.session import SessionData
from app.db.session import Session
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette_prometheus import metrics
from starlette_prometheus import PrometheusMiddleware

app = FastAPI(title=config.PROJECT_NAME, openapi_url="/api/v1/openapi.json")

# CORS
origins = []

# Set all CORS enabled origins
if config.BACKEND_CORS_ORIGINS:
    # origins_raw = config.BACKEND_CORS_ORIGINS.split(",")
    origins_raw = ['http://192.168.99.103:31000', 'http://34.65.150.243:80', 'http://localhost:3000']
    for origin in origins_raw:
        use_origin = origin.strip()
        origins.append(use_origin)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),

app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics/", metrics)

app.include_router(api_v1_router)

SessionData()
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = Session()
    response = await call_next(request)
    request.state.db.close()
    return response