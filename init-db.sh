#!/bin/bash
set -e

# Espera a que PostgreSQL inicie
# until pg_isready -h localhost -p 5432 -U "postgres"; do
#     echo "Waiting for PostgreSQL to start..."
#     sleep 2
# done

# Crea la extensión uuid-ossp
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
EOSQL
