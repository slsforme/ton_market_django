CREATE TABLE IF NOT EXISTS  product_types (
	id SERIAL PRIMARY KEY NOT NULL,
	name VARCHAR(255) NOT NULL UNIQUE CHECK (LENGTH(name) BETWEEN 3 AND 255)
)

CREATE TABLE IF NOT EXISTS roles (
	id SERIAL PRIMARY KEY NOT NULL,
	name VARCHAR(255) NOT NULL UNIQUE CHECK (LENGTH(name) BETWEEN 3 AND 255)
)

CREATE TABLE IF NOT EXISTS products (
	id SERIAL PRIMARY KEY NOT NULL,
	name VARCHAR(255) NOT NULL UNIQUE CHECK (LENGTH(name) BETWEEN 1 AND 255),
	description VARCHAR(1000) NULL, 
	onchain_address VARCHAR(60) NOT NULL UNIQUE CHECK (LENGTH(onchain_address) BETWEEN 40 AND 60),
	owner_address VARCHAR(60) NOT NULL UNIQUE CHECK (LENGTH(owner_address) BETWEEN 40 AND 60),
	metadata TEXT NULL,
	type_id INT NOT NULL,
	FOREIGN KEY (type_id) REFERENCES product_types (id)
)

ALTER TABLE products 
ADD CONSTRAINT check_type_id CHECK (type_id > 0);

ALTER TABLE product_types 
ADD CONSTRAINT check_id CHECK (id > 0);

ALTER TABLE roles  
ADD CONSTRAINT check_id CHECK (id > 0)

ALTER TABLE products 
ADD CONSTRAINT check_id CHECK (id > 0)

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS user_logs (
	id SERIAL PRIMARY KEY NOT NULL CHECK (id > 0),
	user_id INT NOT NULL CHECK (id > 0),
	log_id INT NOT NULL CHECK (id > 0),
	uuid UUID DEFAULT uuid_generate_v4() NOT NULL,
	FOREIGN KEY (log_id) REFERENCES logs (id),
	FOREIGN KEY (user_id) REFERENCES users (id)
)

CREATE TABLE IF NOT EXISTS logs (
    id SERIAL PRIMARY KEY CHECK (id > 0),
    interaction_type VARCHAR(255) NOT NULL CHECK (LENGTH(interaction_type) BETWEEN 3 AND 255),
    created_at TIMESTAMP NOT NULL,
    log_type VARCHAR(255) NOT NULL CHECK (LENGTH(log_type) BETWEEN 3 AND 255),
    name VARCHAR(1000) NOT NULL CHECK (LENGTH(name) BETWEEN 3 AND 1000)
);

ALTER TABLE logs
ALTER COLUMN created_at SET DEFAULT CURRENT_TIMESTAMP;

CREATE OR REPLACE FUNCTION validate_logs_creation_date()
RETURNS TRIGGER AS $$
BEGIN
	IF NEW.created_at < CURRENT_TIMESTAMP THEN
		RAISE EXCEPTION 'created_at cannot be in past!';
	END IF;
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_creating_date
BEFORE INSERT OR UPDATE ON logs 
FOR EACH ROW
EXECUTE FUNCTION validate_logs_creation_date();

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY CHECK (id > 0),
	uuid UUID DEFAULT uuid_generate_v4() NOT NULL,
	login VARCHAR(50) NOT NULL CHECK(LENGTH(login) BETWEEN 5 AND 50),
	password VARCHAR(65) NOT NULL CHECK(LENGTH(password) = 64),
	address VARCHAR(60) NOT NULL UNIQUE CHECK (LENGTH(address) BETWEEN 40 AND 60),
	role_id INT NOT NULL CHECK (id > 0),
	FOREIGN KEY (role_id) REFERENCES roles (id)
)


CREATE TABLE IF NOT EXISTS requests(
    id SERIAL PRIMARY KEY CHECK (id > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	description TEXT NOT NULL CHECK (LENGTH(description) > 7),
	name VARCHAR(255) NOT NULL CHECK (LENGTH(name) BETWEEN 3 and 255),
	email VARCHAR(255) NOT NULL CHECK(LENGTH(email) BETWEEN 7 and 256),
    CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
)

CREATE TABLE IF NOT EXISTS user_requests(
	id SERIAL PRIMARY KEY NOT NULL CHECK (id > 0),
	user_id INT NOT NULL CHECK (id > 0),
	request_id INT NOT NULL CHECK (id > 0),
	uuid UUID DEFAULT uuid_generate_v4() NOT NULL,
	FOREIGN KEY (request_id) REFERENCES requests (id),
	FOREIGN KEY (user_id) REFERENCES users (id)
)

-- TODO: smart contracts, txs, user-txs tables

CREATE TABLE IF NOT EXISTS smart_contracts(
	id SERIAL PRIMARY KEY NOT NULL CHECK (id > 0),
	onchain_address VARCHAR(60) NOT NULL CHECK (LENGTH(onchain_address) BETWEEN 40 AND 60),
	ABI JSONB NULL,
	owner_address VARCHAR(60) NOT NULL CHECK (LENGTH(owner_address) BETWEEN 40 AND 60),
	status VARCHAR(100) NULL,
	createad_at TIMESTAMP NOT NULL,
	uuid UUID DEFAULT uuid_generate_v4() NOT NULL
)

CREATE TABLE IF NOT EXISTS transactions(
	id SERIAL PRIMARY KEY NOT NULL CHECK (id > 0),
	tx_hash VARCHAR(65) NOT NULL CHECK (LENGTH(tx_hash) BETWEEN 63 AND 65),
	smart_contract_id INT NOT NULL CHECK (smart_contract_id > 0),
	type VARCHAR(255) NOT NULL,
	product_id INT NOT NULL CHECK(product_id > 0),
	tx_date TIMESTAMP NOT NULL,
	owner_address VARCHAR(60) NOT NULL CHECK (LENGTH(owner_address) BETWEEN 40 AND 60),
	receiver_address VARCHAR(60) NULL CHECK (LENGTH(receiver_address) BETWEEN 40 AND 60),
	FOREIGN KEY (product_id) REFERENCES products (id),
	FOREIGN KEY (smart_contract_id) REFERENCES smart_contracts (id)
)

CREATE TABLE IF NOT EXISTS user_transactions(
	id SERIAL PRIMARY KEY CHECK (id > 0),
    user_id INT NOT NULL CHECK (id > 0),
	tx_id INT NOT NULL CHECK (id > 0),
	uuid UUID DEFAULT uuid_generate_v4() NOT NULL,
	FOREIGN KEY (tx_id) REFERENCES transactions (id),
	FOREIGN KEY (user_id) REFERENCES users (id)
)


