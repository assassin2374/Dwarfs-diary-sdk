SET client_encoding = 'UTF8';

-- 更新処理
CREATE FUNCTION update_updated_at_column()
  RETURNS TRIGGER AS $$
  BEGIN
      NEW.updated_at = now();
      RETURN NEW;
  END;
  $$ language 'plpgsql';

-- users
CREATE TABLE users (
  id SERIAL NOT NULL,
  name varchar(64) NOT NULL DEFAULT '',
  email varchar(64) NOT NULL DEFAULT '',
  password varchar(200) NOT NULL DEFAULT '',
  created_at TIMESTAMP NOT NULL DEFAULT current_timestamp,
  updated_at TIMESTAMP NOT NULL DEFAULT current_timestamp,
  PRIMARY KEY (id)
);

-- インデックス指定
CREATE UNIQUE INDEX idx_email ON users (email);

-- 更新処理トリガー
CREATE TRIGGER update_user_modtime
  BEFORE UPDATE
  ON users
  FOR EACH ROW
EXECUTE PROCEDURE update_updated_at_column();

-- サンプル
INSERT INTO users (name, email, password) VALUES 
('sam', 'sample01@example.com', 'sample01');

-- diary
CREATE TABLE diary (
  id SERIAL NOT NULL,
  user_id int NOT NULL DEFAULT 0,
  image_id int NOT NULL DEFAULT 0,
  prompt varchar(200) NOT NULL DEFAULT '',
  comment varchar(200) NOT NULL DEFAULT '',
  created_at TIMESTAMP NOT NULL DEFAULT current_timestamp,
  updated_at TIMESTAMP NOT NULL DEFAULT current_timestamp,
  PRIMARY KEY (id),
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (image_id) REFERENCES images(id)
);

-- インデックス指定
CREATE INDEX idx_user_id ON diary (user_id);

-- 更新処理トリガー
CREATE TRIGGER update_diary_modtime
  BEFORE UPDATE
  ON diary
  FOR EACH ROW
EXECUTE PROCEDURE update_updated_at_column();

-- サンプル
INSERT INTO diary (url, impression, user_id, shrine_id) VALUES 
('sample1.com', '故郷', 1, 1), 
('sample2.com', '感謝', 1, 2), 
('sample3.com', '階段', 1, 3);

-- images
CREATE TABLE images (
  id SERIAL NOT NULL,
  user_id int NOT NULL DEFAULT 0,
  shrine_id int NOT NULL DEFAULT 0,
  url varchar(200) NOT NULL DEFAULT '',
  impression varchar(200) NOT NULL DEFAULT '',
  created_at TIMESTAMP NOT NULL DEFAULT current_timestamp,
  updated_at TIMESTAMP NOT NULL DEFAULT current_timestamp,
  PRIMARY KEY (id),
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (shrine_id) REFERENCES shrine(id)
);

-- インデックス指定
CREATE INDEX idx_user_id ON images (user_id);

-- 更新処理トリガー
CREATE TRIGGER update_images_modtime
  BEFORE UPDATE
  ON images
  FOR EACH ROW
EXECUTE PROCEDURE update_updated_at_column();

-- サンプル
INSERT INTO images (url, impression, user_id, shrine_id) VALUES 
('sample1.com', '故郷', 1, 1), 
('sample2.com', '感謝', 1, 2), 
('sample3.com', '階段', 1, 3);

