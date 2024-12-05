from openai import OpenAI
from fastapi import FastAPI, Form, Request
from typing import Annotated
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os

openai = OpenAI(
    api_key= os.getenv('OPENAI_API_KEY')
)

DEFAULT_MODEL = 'gpt-3.5-turbo'
DEFAULT_TEMP = 0.6

app = FastAPI()
templates = Jinja2Templates(directory='templates')

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})



chat_log = [{'role': 'system',
             'content': 'You are a AI system dedicated to helping English speakers '
                        'learn how to Speak Spanish. You will start by learning the user\'s '
                        'experience level and then develop lessons based on that. After each '
                        'lesson you will quiz the user. '
            }]

chat_responses = []

@app.post("/", response_class=HTMLResponse)
async def chatbot(request: Request, user_input: Annotated[str, Form()]):
    chat_log.append({
        'role': 'user',
        'content': user_input
    })
    chat_responses.append(user_input)

    response = openai.chat.completions.create(
        model = DEFAULT_MODEL,
        messages = chat_log,
        temperature = DEFAULT_TEMP
    )

    bot_response = response.choices[0].message.content
    chat_log.append({
        'role': 'assistant',
        'content': bot_response
    })
    chat_responses.append(bot_response)

    return templates.TemplateResponse("home.html", {"request": request, "chat_responses": chat_responses})
