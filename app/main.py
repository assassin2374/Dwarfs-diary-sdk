import io
import os
from PIL import Image
from fastapi import FastAPI
from fastapi.responses import FileResponse
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

# APIインタフェースの準備
stability_api = client.StabilityInference(
    key=os.environ['STABILITY_KEY'],
    verbose=True,
)

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World!!"}

@app.get("/dog_image")
def generate_dog_image():
    # テキストからの画像生成
    answers = stability_api.generate(
        prompt="white dog",
    )
    # 結果の出力
    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                print("NSFW")
            if artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))
                img.save('output.png')
