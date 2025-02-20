import json
import logging
import os
import uuid

logger = logging.getLogger(__name__)

from fastapi import BackgroundTasks, FastAPI, File, HTTPException, Path, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from sherlogholmes.main import kickoff_api

app = FastAPI()

BASE_DIR = "file_server"  
os.makedirs(BASE_DIR, exist_ok=True)

@app.post("/v1/rca/")
async def perform_rca(background_tasks: BackgroundTasks,jobFile: UploadFile = File(...), pyLogs: UploadFile = File(...), nwLogs: UploadFile = File(...),):
    
    task_id = str(uuid.uuid4()) # Generate a unique task ID
    task_dir = os.path.join(BASE_DIR, task_id)
    os.makedirs(task_dir, exist_ok=True)
    for file in [jobFile, pyLogs, nwLogs]:
        contents = await file.read()
        with open(f"./{task_dir}/{file.filename}", "wb") as f:
            f.write(contents)
    
    background_tasks.add_task(kickoff_api, task_id)
    return {"message": "Flow KickOffed", "task_id": task_id}


@app.get("/v1/results/{id}/", response_class=JSONResponse)
async def get_task_results(id: str):
    file_path = os.path.join(BASE_DIR, id, "crew_results.json")

    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="Crew results not found")

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return JSONResponse(content=data)

@app.get("/v1/results/{id}/files")
async def list_task_files(id: str):
    folder_path = os.path.join(BASE_DIR, id)

    if not os.path.isdir(folder_path):
        return {"error": "Folder not found"}

    files = os.listdir(folder_path)
    return {"files": files}

app.mount("/static", StaticFiles(directory=BASE_DIR), name="static")
