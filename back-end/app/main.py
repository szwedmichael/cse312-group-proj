from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .routers import user_auth


app = FastAPI()

# Set CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(user_auth.router)


# https://stackoverflow.com/questions/65916537/a-minimal-fastapi-example-loading-index-html
# https://stackoverflow.com/questions/73911250/how-to-render-css-js-images-along-with-html-file-in-fastapi
app.mount(
    "/", StaticFiles(directory="../front-end/website/dist", html=True), name="static"
)
