from fastapi import FastAPI
from stability_sdk import create_dog_image

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World!!"}

@app.get("/dog_image")
def generate_dog_image():
    image_path = create_dog_image()
    return FileResponse(image_path)
