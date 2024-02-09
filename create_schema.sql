-- Habilitar la extensión uuid-ossp si no está habilitada
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TYPE SIZE_TYPE AS ENUM('LARGE', 'MEDIUM', 'SMALL');

CREATE TABLE IF NOT EXISTS OFFER(
    ID uuid DEFAULT uuid_generate_v4() PRIMARY KEY,
    POSTID VARCHAR(120),
    USERID VARCHAR(40),
    DESCRIPTION VARCHAR(140) NOT NULL,
    SIZE SIZE_TYPE NOT NULL ,
    FRAGILE BOOLEAN NOT NULL,
    OFFER INTEGER NOT NULL,
    CREATEAT timestamp with time zone DEFAULT current_timestamp,
    CONSTRAINT check_offer_positive CHECK(offer >= 0)
);