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
    is_released BOOLEAN DEFAULT TRUE, 
    cover_image CHARACTER VARYING(255)
);

-- 3. Flag: Gizli Kasa (Farklı Tablo)
CREATE TABLE flag (
    id SERIAL PRIMARY KEY,
    flag TEXT 
);

-- --- VERİ GİRİŞİ ---
INSERT INTO users (username,email, password) VALUES 
('Metallica','metallica@gmail.com','SKYDAYS{y3t3r_4rt1k_sqld3n_b1kt1m}'),
('Lady Gaga', 'stefani@ladygaga.com', '827ccb0eea8a706c4c34a16891f84e7b'),
('Batu Akdeniz', 'info@batuakdeniz.com', '098f6bcd4621d373cade4e832627b4f6'),
('Kaptan Kadavra', 'iletisim@kaptankadavra.net', '202cb962ac59075b964b07152d234b70'),
('Venüs', 'venus.official@gmail.com', 'ad0234829205b9033196ba818f7a872b'),
('Necrophagist', 'necrop@gmail.com', '51abb610b806d2d0f507665287f3f61a'),
('James Hetfield', 'papa_het@metallica.com', 'e10adc3949ba59abbe56e057f20f883e'),
('Megadeth','dave@gmail.com','1a1dc91c907325c69271ddf0c944bc72');




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
VALUES ('SKYDAYS{sp4t1fy_sp0t1fyd4n_d4h4_1y1}');

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
