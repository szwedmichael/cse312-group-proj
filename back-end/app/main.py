from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .routers import example

app = FastAPI()

app.include_router(example.router)

# https://stackoverflow.com/questions/65916537/a-minimal-fastapi-example-loading-index-html
# https://stackoverflow.com/questions/73911250/how-to-render-css-js-images-along-with-html-file-in-fastapi
app.mount("/", StaticFiles(directory="app/static/", html=True), name="static")
