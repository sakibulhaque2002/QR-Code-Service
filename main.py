# main.py

from fastapi import FastAPI
from api.endpoints import router  # import the single router
from utils.template_loader import load_templates

app = FastAPI(title="Custom QR Code API")

# Load templates once at startup
app.state.qr_templates = load_templates()

# include the router
app.include_router(router)


