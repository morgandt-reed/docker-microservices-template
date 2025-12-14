# Custom PostgreSQL image with initialization
FROM postgres:15-alpine

# Copy initialization script
COPY init.sql /docker-entrypoint-initdb.d/

# Set locale
ENV LANG=en_US.utf8

# Expose PostgreSQL port
EXPOSE 5432

# Health check
HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
    CMD pg_isready -U ${POSTGRES_USER:-appuser} -d ${POSTGRES_DB:-appdb} || exit 1
