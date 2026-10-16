from fastapi import FastAPI

app = FastAPI(title="Aslan Sultan AI Agent Core")

@app.get("/")
def read_root():
    return {
        "status": "Active",
        "agent": "Aslan Sultan Intelligence Core",
        "message": "Welcome to Aslan Sultan AI Agent API"
    }
