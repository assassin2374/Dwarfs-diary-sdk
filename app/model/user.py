

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