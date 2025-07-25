from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from chainlit.utils import mount_chainlit
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from routes import user as user_routes
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
import uvicorn
#from financial_planner import generate_financial_plan
#from finPalChatNew import FinPalAgent, llm, tools, SYSTEM_MESSAGE_CONTENT,tool_map
app = FastAPI()
Instrumentator().instrument(app).expose(app)

# Include user routes
app.include_router(user_routes.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates directory
templates = Jinja2Templates(directory="templates")

# Route to render the login page
@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Route to render the index page
@app.get("/create")
async def index_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

mount_chainlit(app=app, target="finchat_app.py", path="/chainlit")
# Run the FastAPI app with Uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
