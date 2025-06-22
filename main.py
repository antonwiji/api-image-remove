from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove
from PIL import Image
import base64
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ganti dengan domain frontend kamu untuk keamanan, contoh: ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ImageBase64Request(BaseModel):
    image_base64: str

@app.post("/api/remove-background")
def remove_background_base64(request: ImageBase64Request):
    try:
        # Decode base64 string ke bytes
        image_bytes = base64.b64decode(request.image_base64)

        # Proses hapus background
        output_image_bytes = remove(image_bytes)

        # Buka dan konversi ke base64 lagi
        image = Image.open(io.BytesIO(output_image_bytes))
        img_io = io.BytesIO()
        image.save(img_io, format='PNG')
        img_io.seek(0)

        base64_output = base64.b64encode(img_io.read()).decode('utf-8')
        return {
            "status": "success",
            "image_base64": base64_output
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
