--liquibase formatted sql
--changeset gajendra.sahu:1-create-connection-table
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE connection (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    connection_name VARCHAR(255) NOT NULL,
    host_port VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    description TEXT,
    database VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

--rollback DROP TABLE connection;
--changeset gajendra.sahu:2-create-test-table
CREATE TABLE test (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid()
);

--changeset gajendra.sahu:3-drop-test-table
DROP TABLE IF EXISTS test;