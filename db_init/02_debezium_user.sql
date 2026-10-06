-- ============================================================
-- DEBEZIUM CDC USER
-- ============================================================

CREATE USER debezium WITH
    LOGIN
    REPLICATION
    PASSWORD 'debezium';

GRANT CONNECT ON DATABASE pipeline_db TO debezium;

GRANT USAGE ON SCHEMA public TO debezium;

GRANT SELECT ON ALL TABLES IN SCHEMA public TO debezium;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT ON TABLES TO debezium;