-- Run this file as a PostgreSQL administrator.
-- FastAPI creates all business tables and seed data on startup.

SELECT 'CREATE ROLE yapmitai WITH LOGIN PASSWORD ''yapmitai'''
WHERE NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'yapmitai')
\gexec

SELECT 'CREATE DATABASE yapmitai OWNER yapmitai ENCODING ''UTF8'''
WHERE NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'yapmitai')
\gexec
