from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from rembg import remove
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-netlify-url.netlify.app",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    input_data = await file.read()
    output_data = remove(input_data)
    return StreamingResponse(io.BytesIO(output_data), media_type="image/png")