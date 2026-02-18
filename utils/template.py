# utils/template.py

from fastapi import HTTPException


def get_template(request, template_name: str):
    templates = request.app.state.qr_templates

    if template_name not in templates:
        raise HTTPException(status_code=400, detail="Invalid template name")

    return templates[template_name]
