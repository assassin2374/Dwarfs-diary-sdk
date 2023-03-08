import io
import os
from PIL import Image
from fastapi import FastAPI, Request
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

# APIインタフェースの準備
stability_api = client.StabilityInference(
    key=os.environ['STABILITY_KEY'],
    verbose=True,
)

app = FastAPI()

@app.get("/{prompt}")
def generate_dog_image(prompt:str):
    # テキストからの画像生成
    answers = stability_api.generate(
        prompt=prompt
    )
    # 結果の出力
    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                print("NSFW")
            if artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))
                img.save(prompt+".png")
