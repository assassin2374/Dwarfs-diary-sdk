import io
import os
import uuid
from PIL import Image
from fastapi import FastAPI, Depends
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

from sqlalchemy import Column, Integer, String
from .application import Base, SessionLocal

# Stability APIの呼び出しのためのクライアントオブジェクトを作成する
stability_api = client.StabilityInference(
    key=os.environ['STABILITY_KEY'], # APIキーを環境変数から取得する
    verbose=True, # ログ出力を有効にする
)

# FastAPIのアプリケーションオブジェクトを作成する
app = FastAPI()

# Userクラス定義
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}', password='{self.password}')>"

# Userクラスの依存性注入
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/api/users")
def get_all_users(db: SessionLocal = Depends(get_db)):
    users = db.query(User).all()
    return {"users": users}

# APIエンドポイントを定義する
@app.get("/prompt={prompt}")
def generate_image(prompt:str):
    # テキストからの画像生成を行う
    answers = stability_api.generate(prompt=prompt)

    # 生成された画像を保存するための処理を行う
    for resp in answers:
        for artifact in resp.artifacts:
            # NSFW画像が生成された場合の処理
            if artifact.finish_reason == generation.FILTER:
                print("NSFW")
            # 生成された画像がPNGファイルの場合の処理
            if artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))

                # UUIDでファイル名を生成する
                filename = str(uuid.uuid4()) + '.png'

                # PILライブラリを使ってPNGファイルを保存する
                img.save(filename +".png")
