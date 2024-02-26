from starlette.responses import FileResponse


# Long things like db queries and long stuff go in repo
class ExampleRepo:
    def __init__(self):
        pass

    # https://stackoverflow.com/questions/65916537/a-minimal-fastapi-example-loading-index-html
    def get_index(self):
        return FileResponse("../front-end/index.html")
