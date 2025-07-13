SELECT 'CREATE DATABASE app' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'app')\gexec
\c app

SELECT 'CREATE SCHEMA educa_mais' WHERE NOT EXISTS (SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'educa_mais')\gexec