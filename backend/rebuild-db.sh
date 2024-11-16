export PGPASSWORD=changethis
psql -h localhost -U postgres -c "drop database if exists app;"
psql -h localhost -U postgres -c "create database app;"
psql -h localhost -U postgres -d app -c "create extension ltree;"
