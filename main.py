import os

from typing import Annotated
from gigachat import GigaChat
from dotenv import load_dotenv

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

load_dotenv()

app = FastAPI()

templates = Jinja2Templates(directory="templates")

AUTH_KEY = os.getenv('AUTH_KEY')

@app.post("/question")
async def get_data_from_form(request: Request, question: Annotated[str, Form()]):
    print('get question: ', question)
    with GigaChat(
        credentials=AUTH_KEY,
        scope='GIGACHAT_API_PERS',
        verify_ssl_certs=False
    ) as giga:
        response = giga.chat(question)
    text_response = response.choices[0].message.content
    print('giga response', text_response)
    reply = text_response
    return templates.TemplateResponse(
        request=request,
        name="item.html",
        context={'reply': reply},
    )
    # return RedirectResponse('/', status_code=302)


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="item.html",
    )