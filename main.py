from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove
from PIL import Image
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with Netlify URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    try:
        image_data = await file.read()
        
        # Resize large images to prevent OOM
        image = Image.open(io.BytesIO(image_data))
        image.thumbnail((1024, 1024))

        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        resized_image_data = buffer.read()

        output = remove(resized_image_data)
        return StreamingResponse(io.BytesIO(output), media_type="image/png")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
