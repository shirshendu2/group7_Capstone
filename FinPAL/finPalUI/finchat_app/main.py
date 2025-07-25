from fastapi import FastAPI
from chainlit.utils import mount_chainlit
from prometheus_fastapi_instrumentator import Instrumentator
import uvicorn
#from financial_planner import generate_financial_plan
#from finPalChatNew import FinPalAgent, llm, tools, SYSTEM_MESSAGE_CONTENT,tool_map
app = FastAPI()
Instrumentator().instrument(app).expose(app)

mount_chainlit(app=app, target="finchat_app.py", path="/chainlit")
# Run the FastAPI app with Uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
