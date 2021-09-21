# Blog Portal
Blog Portal is test project on Django using Docker.

## Data Base
In docker/postgres find init.sql file. Write your own settings in it.
``` sql
CREATE USER user WITH PASSWORD password;

CREATE DATABASE database;
GRANT ALL PRIVILEGES ON DATABASE database TO user;
```

## Settings
Create a ".env" file as in example "env.example"

Or

Write your own local env settings in config/settings.py

```python
env = environ.Env(
    DJANGO_DEBUG=(bool, False),
    DJANGO_SECRET_KEY=(str, 'CHANGEME!!!e8!1671ifpp362f9gbd3v@e($0_flznbb3fa2d4zg7zn@%yyk2'),
    DJANGO_ALLOWED_HOSTS=(list, ["*"]),
    DJANGO_DATABASE_URL=(str, 'postgres://USER:PASSWORD@posgresdb:PORT/blog_portal'),
)
```

## Create image
Use docker-compose to create docker image
```docker
docker-compose build --no-cache
```
## Run container
Use docker compose to run docker container
```docker
docker-compose up
```

### To run without Docker

## Install packages
Use the package manager pip to install all package from requirements.txt
```shell
pip3 install -r requirements.txt
```
## Migrate
Apply all migrations into your DB
```shell
python manage.py migrate
```
