from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .routers import user_auth, manage_post, homepage
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request


app = FastAPI()


# https://stackoverflow.com/questions/62928450/how-to-put-backend-and-frontend-together-returning-react-frontend-from-fastapi
# Sets the templates directory to the `build` folder from `npm run build`
# this is where you'll find the index.html file.
dist_dir = "../front-end/website/dist"
templates = Jinja2Templates(directory=dist_dir)
# Mounts the `assets` folder within the `build` folder to the `/assets` route.
app.mount("/assets", StaticFiles(directory=f"{dist_dir}/assets"), name="assets")


# Defines a route handler for `/*` essentially.
# NOTE: this needs to be the last route defined b/c it's a catch all route
@app.get("/{rest_of_path:path}")
async def react_app(req: Request, rest_of_path: str):
    return templates.TemplateResponse("index.html", {"request": req})


# Set CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(user_auth.router)
app.include_router(manage_post.router)
app.include_router(homepage.router)
