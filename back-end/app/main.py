from fastapi import FastAPI, Response, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .routers import user_auth, manage_post, homepage
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import FileResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

app = FastAPI()


limiter = Limiter(key_func=get_remote_address, default_limits=["50/10seconds"])
app.state.limiter = limiter


async def _rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    raise HTTPException(status_code=429, detail="Too many requests")


app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.middleware("http")
@limiter.limit("50/10seconds")  # 50 / 10 seconds
async def add_process_time_header(request: Request, call_next):
    response = await call_next(request)
    return response


# https://stackoverflow.com/questions/62928450/how-to-put-backend-and-frontend-together-returning-react-frontend-from-fastapi
# Sets the templates directory to the `build` folder from `npm run build`
# this is where you'll find the index.html file.
dist_dir = "app/static/dist"
templates = Jinja2Templates(directory=dist_dir)


# https://stackoverflow.com/questions/75299908/how-to-add-custom-headers-to-static-files-in-fastapi
@app.get("/assets/{file_path:path}")
async def assets(file_path: str):
    response = FileResponse(f"{dist_dir}/assets/{file_path}")
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


# Mount the static folder to be served at '/static' URL path
app.mount("/app/static", StaticFiles(directory="app/static/"), name="static")

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


# Defines a route handler for `/*` essentially.
# NOTE: this needs to be the last route defined b/c it's a catch all route
@app.get("/{rest_of_path:path}")
async def react_app(response: Response, req: Request, rest_of_path: str):
    response = templates.TemplateResponse("index.html", {"request": req})
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response
