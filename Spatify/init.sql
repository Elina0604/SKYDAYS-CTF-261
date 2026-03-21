-- --- TABLO OLUŞTURMA ---

-- 1. Flag: Kullanıcı Veritabanı
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL
);

-- 2. Flag: Şarkı Kataloğu
CREATE TABLE songs (
    id SERIAL PRIMARY KEY,
    artist TEXT NOT NULL,
    song_title TEXT NOT NULL,
    is_released BOOLEAN DEFAULT TRUE, -- Flag 2: skydays{unr3l34s3d_un1on_h1t}
    cover_image CHARACTER VARYING(255)
);

-- 3. Flag: Gizli Kasa (Farklı Tablo)
CREATE TABLE flag (
    id SERIAL PRIMARY KEY,
    flag TEXT -- Flag 3: skydays{t1m3_b4s3d_v4ult_77}
);

-- --- VERİ GİRİŞİ ---
INSERT INTO users (username,email, password) VALUES 
('admin','admin@gmail.com','SKYDAYS{y3t3r_4rt1k_sqld3n_b1kt1m}');



INSERT INTO songs (artist, song_title, is_released, cover_image) VALUES 
('Metallica', 'Wherever I May Roam', TRUE ,'wherever.jpg'),
('Megadeth', 'Addicted To Chaos', TRUE , 'tout.jfif'),
('Lady Gaga', 'Dead Dance', TRUE , 'lady.png'),
('Batu Akdeniz', 'Ankara''nın Sokaklarında', TRUE , 'batu.jfif'),
('Kaptan Kadavra', 'Katarakt', TRUE , 'kaptan.jpg'),
('SkyDays', 'skydays_leaked_hit', FALSE , 'sql.jpg'),
('Venüs', 'Cehennem', TRUE , 'venüs.jfif'),
('Necrophagist', 'Stabwound', TRUE , 'necrop.jpg');



INSERT INTO flag (flag) 
VALUES ('SKYDAYS{3_h4rfl1l3r_s0rusu_0ldu}');

-- --- YETKİLENDİRME (RBAC) ---

-- Kamu erişimini tamamen kapatıyoruz (Şemayı görmesinler)
REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT USAGE ON SCHEMA public TO PUBLIC;

-- 1. AGENT: login_agent (Sadece Users tablosu)
CREATE USER agent_login WITH PASSWORD 'pass_login_77';
GRANT SELECT ON TABLE users TO agent_login;

CREATE USER agent_flag WITH PASSWORD 'pass_flag_98';
GRANT SELECT ON TABLE flag TO agent_flag;
GRANT SELECT ON TABLE songs TO agent_flag;
-- 3. AGENT: sort_agent (Songs + Secret Vault)
-- Not: Sort işlemi songs üzerinden yapıldığı için songs'u da görmeli
CREATE USER agent_sort WITH PASSWORD 'pass_sort_99';
GRANT SELECT ON TABLE songs TO agent_sort;
