#!/bin/sh

# Check if the database is PostgreSQL
if [ "$DATABASE" = "postgres" ]
then
    # Print a message indicating that the script is waiting for PostgreSQL
    echo "Waiting for postgres..."
    
    # Loop until a connection can be established to the database host and port
    while ! nc -z $SQL_HOST $SQL_PORT; do
      # Sleep for short duration before checking again
      sleep 0.1
    done
    
    # Return that PostgreSQL is up and running 
    echo "PostgreSQL started"
fi

# Execute the command or application specified as arguments to the script
exec "$@"