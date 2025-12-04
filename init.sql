
CREATE TABLE IF NOT EXISTS "user" ( 
	id SERIAL PRIMARY KEY, 
	email VARCHAR(150) UNIQUE NOT NULL, 
	password_hash VARCHAR(200) NOT NULL, 
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
	); 
	
CREATE TABLE IF NOT EXISTS product ( 
	id SERIAL PRIMARY KEY, 
	nome VARCHAR(100) NOT NULL, 
	marca VARCHAR(100) NOT NULL, 
	valor NUMERIC(10,2) NOT NULL, 
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
	updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
	); 

-- Usuário inicial: email admin@test.com, senha "123456" (hash gerada com bcrypt) 
INSERT INTO "user" (email, password_hash) 
VALUES ('admin@test.com', '$2b$12$NwkB0Iv0j1dvf82e.H4CyufkddQ4paL6I7FNZIk53SLnQjmEMYe0.');