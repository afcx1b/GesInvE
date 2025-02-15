-- Crear usuario admin como superusuario
CREATE USER admin WITH PASSWORD 'Ptf8454Jd55' SUPERUSER;

-- Crear usuario inven
CREATE USER inven WITH PASSWORD 'Inv#2435';

-- Crear usuario user
CREATE USER user WITH PASSWORD 'User#5494';

-- Otorgar permisos necesarios a los usuarios
GRANT ALL PRIVILEGES ON DATABASE tu_base_de_datos TO admin;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO inven;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO user;