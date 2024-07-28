from typing import Union
import asyncio
import concurrent.futures
from fastapi import FastAPI, Request  
from fastapi.responses import HTMLResponse                      
import time
import uvicorn
from starlette.concurrency import run_in_threadpool
app = FastAPI()
import anyio
from contextlib import asynccontextmanager
from anyio.lowlevel import RunVar
from anyio import CapacityLimiter
import os
import uvloop
from fastapi.staticfiles import StaticFiles
# import hypercorn
import cProfile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")
count = 0

import asyncio

processQ = asyncio.Queue()

async def wt(scope: dict, receive: callable, send: callable):
    # Your WebTransport handler logic here
    pass

    # @app.middleware("http")
    # async def webtransport_middleware(request: Request, call_next):
    #     if request.scope["type"] == "webtransport" and request.scope["path"] == "/wt":
    #         await wt(request.scope, request.receive, request.send)
    #     else:
    #         response = await call_next(request)
    #         return response

def sighandler():
    print(os.getpid())
# ROOT = os.path.dirname(__file__)
# STATIC_ROOT = os.environ.get("STATIC_ROOT", os.path.join(ROOT, "htdocs"))
@asynccontextmanager
async def startup(app: FastAPI):
    global count
    print(f"started with {os.getpid()}")
    RunVar("_default_thread_limiter").set(CapacityLimiter(2000))
    yield
    print(f"exiting with {count} requests handled")
    raise KeyboardInterrupt
    

# loop = asyncio.get_event_loop()
# loop.add_signal_handler(sig=2,callback=sighandler)
app = FastAPI(lifespan=startup)
app.mount("/htdocs", StaticFiles(directory="htdocs"), name="htdocs")

@app.get("/",response_class=HTMLResponse)
async def _(request: Request):
    # await request.send_push_promise("/style.css")
    # await request.send_push_promise("/scripts/index.js")
    return templates.TemplateResponse("index.html",{"request":request})


@app.get("/1")
async def read_root():
    global count
    print("Hello")
    await asyncio.sleep(2)
    print("ball")
    count = count +1
    return {"Hello": "World"}

@app.get("/2")
def read_root():
    global count
    print("Hello")
    time.sleep(2)
    print("World")
    count = count +1
    return {"Hello": "World"}

@app.get("/3")
async def read_root():
    global count
    print("Hello")
    # with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    #     future = executor.submit(blocking)
    await run_in_threadpool(blocking)
    count = count +1
    return {"Hello": "World"}

def blocking():
    time.sleep(2)
    print("World")
    
async def consumer():
    while True:
        try:
            msg = await processQ.get()
            print(msg)
        except Exception as e:
            print(e)

async def main():
    async with asyncio.TaskGroup() as tg:
        tg.create_task(consumer())
        tg.create_task(hypercorn.asyncio.serve(app,config=hyp_config))



# if __name__ == "__main__":
    # uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="debug", reload=False,
    #             workers=2)
    
    # hyp_config = hypercorn.Config()
    # hyp_config.bind = ['0.0.0.0:8000']
    # hyp_config.loglevel = "DEBUG"
    # hyp_config.worker_class = "uvloop"
    # hyp_config.workers = 3

    # with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
    #     try:
    #         runner.run(main())
    #         runner.close()
    #     except KeyboardInterrupt as e:
    #         print("Exit")
    #         runner.close()