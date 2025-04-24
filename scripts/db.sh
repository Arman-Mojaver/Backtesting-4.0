#!/bin/bash

set -e

ACTION=$1         # dump or load
ENVIRONMENT=$2    # development or production

if [[ -z "$ACTION" || -z "$ENVIRONMENT" ]]; then
  echo "Usage: ./db.sh [dump|load] [development|production]"
  exit 1
fi

CONTAINER="db-$ENVIRONMENT"
DATABASE="db-$ENVIRONMENT"
DUMP_DIR="db_dumps"
TIMESTAMP=$(date +"%Y%m%d_%H%M")
DUMP_FILE_NAME="db_${ENVIRONMENT}_${TIMESTAMP}.dump"
DUMP_FILE_LATEST="db_${ENVIRONMENT}_latest.dump"

if [[ "$ACTION" == "dump" ]]; then
  echo "🔄 Dumping $DATABASE from container $CONTAINER..."
  docker exec -t "$CONTAINER" pg_dump -U postgres -F c -d "$DATABASE" -f "/tmp/$DUMP_FILE_NAME"
  docker cp "$CONTAINER:/tmp/$DUMP_FILE_NAME" "$DUMP_DIR/$DUMP_FILE_NAME"
  cp "$DUMP_DIR/$DUMP_FILE_NAME" "$DUMP_DIR/$DUMP_FILE_LATEST"  # overwrite latest
  docker exec "$CONTAINER" rm "/tmp/$DUMP_FILE_NAME"
  echo "✅  Dump complete: $DUMP_DIR/$DUMP_FILE_NAME"

elif [[ "$ACTION" == "load" ]]; then
  echo "♻️ Restoring latest dump to $DATABASE in container $CONTAINER..."

  docker cp "$DUMP_DIR/$DUMP_FILE_LATEST" "$CONTAINER:/tmp/$DUMP_FILE_LATEST"

  if [[ "$ENVIRONMENT" == "development" ]]; then
    echo "🧨 Dropping and recreating $DATABASE (development only)..."
    # Terminate active connections before dropping the database
    docker exec "$CONTAINER" psql -U postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '$DATABASE' AND pid <> pg_backend_pid();"
    docker exec "$CONTAINER" psql -U postgres -c "DROP DATABASE IF EXISTS \"$DATABASE\""
    docker exec "$CONTAINER" psql -U postgres -c "CREATE DATABASE \"$DATABASE\""
  else
    echo "🔒 Production: will not drop $DATABASE — ensuring it exists..."
    docker exec "$CONTAINER" psql -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = '$DATABASE'" | grep -q 1 || \
      docker exec "$CONTAINER" psql -U postgres -c "CREATE DATABASE \"$DATABASE\""
  fi

  docker exec -i "$CONTAINER" pg_restore -U postgres -d "$DATABASE" "/tmp/$DUMP_FILE_LATEST"
  docker exec "$CONTAINER" rm "/tmp/$DUMP_FILE_LATEST"
  echo "✅  Load complete for $DATABASE"

else
  echo "❌  Unknown action: $ACTION"
  exit 1
fi
