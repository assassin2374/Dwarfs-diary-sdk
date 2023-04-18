import io
import os
import uuid
from PIL import Image
from fastapi import FastAPI, Depends, HTTPException
from .application import SessionLocal
from typing import List
from . import models, schemas
# stable_diffusion_sdk
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

# Stability APIの呼び出しのためのクライアントオブジェクトを作成する
stability_api = client.StabilityInference(
    key=os.environ['STABILITY_KEY'], # APIキーを環境変数から取得する
    verbose=True, # ログ出力を有効にする
)

# FastAPIのアプリケーションオブジェクトを作成する
app = FastAPI()

# Userクラスの依存性注入
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# 全ユーザー取得API
@app.get("/api/users", response_model=List[schemas.User])
def get_all_users(db: SessionLocal = Depends(get_db)):
    users = db.query(models.User).all()
    return users

# 特定ユーザー取得API
@app.get("/api/user/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: SessionLocal = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# ユーザー登録API
@app.post("/api/user", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: SessionLocal = Depends(get_db)):
    db_user = models.User(name=user.name, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# ユーザー更新API
@app.put("/api/user/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate, db: SessionLocal = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.name = user.name
    db_user.email = user.email
    db_user.password = user.password
    db.commit()
    db.refresh(db_user)
    return db_user

# ユーザー削除API
@app.delete("/api/user/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: SessionLocal = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user

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
