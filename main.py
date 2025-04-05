from fastapi import FastAPI,Form
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from diffusers import StableDiffusionPipeline
import torch
import uuid
import os

app = FastAPI()

# Enable CORS so frontend can access the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the model
device = "cuda" if torch.cuda.is_available() else "cpu"
pipe = StableDiffusionPipeline.from_pretrained(
    "CompVis/stable-diffusion-v1-4",
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
)
pipe = pipe.to(device)

# Create output folder
os.makedirs("generated_images", exist_ok=True)

@app.post("/text-to-image/")
async def text_to_image(
    prompt: str = Form(...),
    negative_prompt: str = Form(None),
    guidance_scale: float = Form(7.5),
    num_inference_steps: int = Form(50)
):
    try:
        # Generate image with advanced parameters
        image = pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            guidance_scale=guidance_scale,
            num_inference_steps=num_inference_steps
        ).images[0]

        # Save the image
        filename = f"{uuid.uuid4().hex[:8]}.png"
        filepath = os.path.join("generated_images", filename)
        image.save(filepath)

        return FileResponse(filepath, media_type="image/png", filename=filename)

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# Run the appif __name__ == "__main__":
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)