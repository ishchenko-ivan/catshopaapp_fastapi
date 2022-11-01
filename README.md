# CatShopApp Project

#### Prerequisites
- Docker ([Docker installation guide](https://docs.docker.com/install/#supported-platforms));
- Docker Compose ([Docker Compose installation guide](https://docs.docker.com/compose/install/)).

#### Configuring Local Environment
Build container
```bash
$ docker build catshopapp_project .
```

Run application
```bash
$ docker-compose up
```

Run application detached console
```bash
$ docker-compose up -d
```

#### Alembic (migrations)
Autogenerate
```bash
$ docker-compose exec catshopapp python -m alembic revision --autogenerate -m "The first revision! Again!"
```

Run migrations
```bash
$ docker-compose exec catshopapp python -m alembic upgrade head
```

Downgrade migrations (-1 - how many revisions downgrade)
```bash
$ docker-compose exec catshopapp python -m alembic downgrade -1
```

# Rule #1 is that you gotta have fun