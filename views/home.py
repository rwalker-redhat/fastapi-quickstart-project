import fastapi
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from typing import Optional

router = fastapi.APIRouter()
templates = Jinja2Templates('templates')


env_string: Optional[str] = None


@router.get('/')
def home(request: Request):
    return templates.TemplateResponse('home.html', {'request': request, 'env_string': env_string})
