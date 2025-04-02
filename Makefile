SHELL := /bin/bash # Use bash syntax

# Carrega variáveis do .env principal se existir
ifneq (,$(wildcard .env))
	include .env
	export
endif

# Carrega variáveis específicas da base de dados com base no ENVIRONMENT
ifneq (,$(wildcard backend/.env.${ENVIRONMENT}))
	include backend/.env.${ENVIRONMENT}
	export
endif

ARG := $(word 2, $(MAKECMDGOALS) )
DOCKER_COMPOSE_FILE := docker-compose.${ENVIRONMENT}.yml

clean:
	@find . -name "*.pyc" -exec rm -rf {} \;
	@find . -name "__pycache__" -delete

test:
	poetry run backend/manage.py test backend/ $(ARG) --parallel --keepdb

test_reset:
	poetry run backend/manage.py test backend/ $(ARG) --parallel

backend_format:
	black backend

docker_setup:
	@echo -e "\033[32m[SETUP] Criando volume da base de dados\033[0m"
	docker volume create romweb_dbdata
	@echo -e "\033[32m[SETUP]Configurando Backend\033[0m"
	docker-compose -f $(DOCKER_COMPOSE_FILE) build --no-cache backend
	docker-compose -f ${DOCKER_COMPOSE_FILE} run --rm backend python manage.py spectacular --color --file schema.yml
	@echo -e "\033[32m[SETUP]Configurando Frontend\033[0m"
	docker-compose -f ${DOCKER_COMPOSE_FILE} run frontend npm install
	docker-compose -f ${DOCKER_COMPOSE_FILE} run --rm frontend npm run openapi-ts

docker_test:
	docker-compose -f ${DOCKER_COMPOSE_FILE} run backend python manage.py test $(ARG) --parallel --keepdb

docker_test_reset:
	docker-compose -f ${DOCKER_COMPOSE_FILE} run backend python manage.py test $(ARG) --parallel

docker_wipe:
	sudo chown -R ${USER}:${USER} .
	@git clean -fd
	@rm -rf backend/staticfiles/ frontend/webpack_bundles/
	@docker system prune -a --volumes -f
	@docker volume ls -qf dangling=true | xargs -r docker volume rm

docker_clean:
	sudo chown -R ${USER}:${USER} .
	@rm -rf frontend/webpack_bundles/
	@docker system prune -a --volumes -f
	@docker volume ls -qf dangling=true | xargs -r docker volume rm

docker_dev_up:
	docker-compose -f ${DOCKER_COMPOSE_FILE} up -d

docker_prod_up:
	@echo -e "\033[32m[INFO] Iniciando a atualização dos contêineres com Rolling Update...\033[0m"
	@docker-compose -f ${DOCKER_COMPOSE_FILE} up -d --no-deps backend
	@docker-compose -f ${DOCKER_COMPOSE_FILE} up -d --no-deps frontend
	@echo -e "\033[32m[INFO] Construindo o frontend com Webpack...\033[0m"
	@docker-compose -f ${DOCKER_COMPOSE_FILE} run --rm frontend npm run build
	@echo -e "\033[32m[INFO] Coletando os arquivos estáticos para o Django...\033[0m"
	@docker-compose -f ${DOCKER_COMPOSE_FILE} run --rm backend poetry run ./manage.py collectstatic --clear --noinput
	@echo -e "\033[32m[INFO] Aguardando as novas versões estarem ativas...\033[0m"
	@docker-compose -f ${DOCKER_COMPOSE_FILE} up -d --no-deps --scale backend=2
	@docker-compose -f ${DOCKER_COMPOSE_FILE} up -d --no-deps --scale frontend=2
	@echo -e "\033[32m[INFO] Contêineres atualizados!\033[0m"

docker_update_dependencies:
	docker-compose -f ${DOCKER_COMPOSE_FILE} down
	docker-compose -f ${DOCKER_COMPOSE_FILE} up -d --build

docker_down:
	docker-compose -f ${DOCKER_COMPOSE_FILE} down

docker_logs:
	docker-compose -f ${DOCKER_COMPOSE_FILE} logs -f $(ARG)

docker_makemigrations:
	docker-compose -f ${DOCKER_COMPOSE_FILE} run --rm backend python manage.py makemigrations

docker_migrate:
	docker-compose -f ${DOCKER_COMPOSE_FILE} run --rm backend python manage.py migrate

docker_backend_shell:
	docker-compose -f ${DOCKER_COMPOSE_FILE} run --rm backend bash

docker_backend_update_schema:
	docker-compose -f ${DOCKER_COMPOSE_FILE} run --rm backend python manage.py spectacular --color --file schema.yml

docker_frontend_update_api:
	docker-compose -f ${DOCKER_COMPOSE_FILE} run --rm frontend npm run openapi-ts

docker_db_save:
	@mkdir -p backend/checkpoint/db
	@DATE=$$(date +"%Y-%m-%d_%H-%M-%S") && \
	docker-compose -f ${DOCKER_COMPOSE_FILE} exec db sh -c "pg_dump -U ${POSTGRES_USER} -d ${POSTGRES_DB} --clean --create > db-backup.sql" && \
	docker cp $$(docker-compose -f ${DOCKER_COMPOSE_FILE} ps -q db):db-backup.sql backend/checkpoint/db/$$DATE-db-backup.sql && \
	echo "Backup salvo em backend/checkpoint/db/$$DATE-db-backup.sql"
	@ls -tp backend/checkpoint/db/ | grep -v '/$$' | tail -n +4 | xargs -I {} rm -- "backend/checkpoint/db/{}"

docker_db_restore:
	@LAST_BKP=$$(ls -t backend/checkpoint/db | grep "db-backup.sql" | head -n 1) && \
	echo "Restaurando a partir de backend/checkpoint/db/$$LAST_BKP" && \
	docker cp backend/checkpoint/db/$$LAST_BKP $$(docker-compose -f ${DOCKER_COMPOSE_FILE} ps -q db):/tmp/db-backup.sql && \
	docker-compose -f ${DOCKER_COMPOSE_FILE} exec db sh -c "psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} < /tmp/db-backup.sql"
	@echo "Restauração concluída!"

deploy_rolling_update:
	@echo -e "\033[32m[DEPLOY] Iniciando Rolling Update...\033[0m"
	@make docker_setup  
	@echo -e "\033[32m[DEPLOY] Rodando os containers...\033[0m"
	@make docker_prod_up  
	@echo -e "\033[32m[DEPLOY] Atualizando a base de dados...\033[0m"
	@make docker_db_restore  
	@echo -e "\033[32m[DEPLOY] Rolling Update concluído!\033[0m"

