.PHONY: clean backend_format docker_create_db_volume docker_up_build docker_build_backend docker_build_frontend docker_update_schema docker_down docker_dev_up docker_logs docker_backend_shell docker_makemigrations docker_migrate docker_frontend_update_api docker_test docker_test_reset docker_db_save docker_db_restore docker_wipe docker_cleanup_frontend docker_setup docker_update_dependencies docker_prod_up deploy_rolling_update

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

# ==== Targets Básicos ====

clean:
	@echo -e "\033[32m[INFO] Limpando arquivos .pyc e __pycache__\033[0m"
	@find . -name "*.pyc" -exec rm -rf {} \;
	@find . -name "__pycache__" -delete

backend_format:
	@echo -e "\033[32m[INFO] Formatando código Python com Black\033[0m"
	docker-compose -f ${DOCKER_COMPOSE_FILE} run backend black .

git_update_submodules:
	@echo -e "\033[32m[INFO] Atualizando Submodules recursivamente\033[0m"
	git submodule update --remote --merge --recursive

docker_create_db_volume:
	@echo -e "\033[32mCriando volume Docker para o banco de dados\033[0m"
	docker volume create romweb_dbdata

docker_create_dev_network:
	@echo -e "\033[32mCriando Rede Docker para comunicação entre serviços.\033[0m"
	docker network create romweb_dev_network
	
docker_up_build:
	docker-compose -f ${DOCKER_COMPOSE_FILE} up -d --build

docker_build_backend:
	@echo -e "\033[32m[INFO] Buildando container Backend\033[0m"
	docker-compose -f ${DOCKER_COMPOSE_FILE} build --no-cache backend

docker_build_frontend:
	@echo -e "\033[32m[INFO] Instalando dependências e atualizando OpenAPI no Frontend\033[0m"
	docker-compose -f ${DOCKER_COMPOSE_FILE} run frontend npm install
	docker-compose -f ${DOCKER_COMPOSE_FILE} run --rm frontend npm run openapi-ts

docker_update_schema:
	@echo -e "\033[32m[INFO] Gerando arquivo de schema OpenAPI (schema.yml)\033[0m"
	docker-compose -f ${DOCKER_COMPOSE_FILE} run --rm backend python manage.py spectacular --color --file schema.yml

docker_down:
	@echo -e "\033[32m[INFO] Parando e removendo containers\033[0m"
	docker-compose -f ${DOCKER_COMPOSE_FILE} down

docker_dev_up:
	@echo -e "\033[32m[INFO] Subindo ambiente de desenvolvimento\033[0m"
	docker-compose -f ${DOCKER_COMPOSE_FILE} up -d

docker_logs:
	@echo -e "\033[32m[INFO] Exibindo logs do serviço $(ARG)\033[0m"
	docker-compose -f ${DOCKER_COMPOSE_FILE} logs -f $(ARG)

docker_backend_shell:
	@echo -e "\033[32m[INFO] Abrindo shell interativo no backend\033[0m"
	docker-compose -f ${DOCKER_COMPOSE_FILE} run --rm backend bash

docker_makemigrations:
	@echo -e "\033[32m[INFO] Criando novas migrações Django\033[0m"
	docker-compose -f ${DOCKER_COMPOSE_FILE} run --rm backend python manage.py makemigrations $(ARG)

docker_migrate:
	@echo -e "\033[32m[INFO] Aplicando migrações Django\033[0m"
	docker-compose -f ${DOCKER_COMPOSE_FILE} run --rm backend python manage.py migrate $(ARG)

docker_frontend_update_api:
	@echo -e "\033[32m[INFO] Atualizando clientes TypeScript com OpenAPI\033[0m"
	docker-compose -f ${DOCKER_COMPOSE_FILE} run --rm frontend npm run openapi-ts

docker_test:
	@echo -e "\033[32m[INFO] Executando testes com keepdb\033[0m"
	docker-compose -f ${DOCKER_COMPOSE_FILE} run backend python manage.py test -v 2 $(ARG) --parallel --keepdb

docker_test_reset:
	@echo -e "\033[32m[INFO] Executando testes com recriação de base\033[0m"
	docker-compose -f ${DOCKER_COMPOSE_FILE} run backend python manage.py test -v 2 $(ARG) --parallel

# ==== Backup / Restore ====

docker_db_save:
	@echo -e "\033[32m[INFO] Gerando backup do banco de dados\033[0m"
	@mkdir -p backend/checkpoint/db
	@DATE=$$(date +"%Y-%m-%d_%H-%M-%S") && \
	docker-compose -f ${DOCKER_COMPOSE_FILE} exec db sh -c "pg_dump -U ${POSTGRES_USER} -d ${POSTGRES_DB} --clean --create > db-backup.sql" && \
	docker cp $$(docker-compose -f ${DOCKER_COMPOSE_FILE} ps -q db):db-backup.sql backend/checkpoint/db/$$DATE-db-backup.sql && \
	echo "Backup salvo em backend/checkpoint/db/$$DATE-db-backup.sql"
	@ls -tp backend/checkpoint/db/ | grep -v '/$$' | tail -n +4 | xargs -I {} rm -- "backend/checkpoint/db/{}"

docker_db_restore:
	@echo -e "\033[32m[INFO] Restaurando banco de dados a partir do último backup\033[0m"
	@LAST_BKP=$$(ls -t backend/checkpoint/db | grep "db-backup.sql" | head -n 1) && \
	echo "Restaurando a partir de backend/checkpoint/db/$$LAST_BKP" && \
	docker cp backend/checkpoint/db/$$LAST_BKP $$(docker-compose -f ${DOCKER_COMPOSE_FILE} ps -q db):/tmp/db-backup.sql && \
	docker-compose -f ${DOCKER_COMPOSE_FILE} exec db sh -c "psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} < /tmp/db-backup.sql"
	@echo "Restauração concluída!"

# ==== Limpezas ====

docker_wipe:
	@echo -e "\033[32m[INFO] Limpeza completa de imagens, volumes e arquivos locais\033[0m"
	sudo chown -R ${USER}:${USER} .
	@git clean -fd
	@rm -rf backend/staticfiles/ frontend/webpack_bundles/
	@docker system prune -a --volumes -f
	@docker volume ls -qf dangling=true | xargs -r docker volume rm

docker_cleanup_frontend:
	@echo -e "\033[32m[INFO] Parando e removendo container frontend\033[0m"
	@docker-compose -f ${DOCKER_COMPOSE_FILE} stop frontend
	@docker-compose -f ${DOCKER_COMPOSE_FILE} rm -sf frontend
	
# ==== Targets Compostos ====

docker_setup:
	$(MAKE) docker_create_db_volume
	$(MAKE) docker_build_backend
	$(MAKE) docker_update_schema
	$(MAKE) docker_build_frontend

docker_update_dependencies:
	$(MAKE) docker_down
	$(MAKE) docker_up_build

docker_prod_up:
	@echo -e "\033[32m[INFO] Rolling Update Backend e Frontend\033[0m"
	@docker-compose -f ${DOCKER_COMPOSE_FILE} up -d --no-deps backend
	@docker-compose -f ${DOCKER_COMPOSE_FILE} up -d --no-deps frontend
	@echo -e "\033[32m[INFO] Buildando Frontend\033[0m"
	@docker-compose -f ${DOCKER_COMPOSE_FILE} run --rm frontend npm run build
	@echo -e "\033[32m[INFO] Coletando staticfiles\033[0m"
	@docker-compose -f ${DOCKER_COMPOSE_FILE} run --rm backend poetry run ./manage.py collectstatic --clear --noinput
	@echo -e "\033[32m[INFO] Escalando Backend\033[0m"
	@docker-compose -f ${DOCKER_COMPOSE_FILE} up -d --no-deps --scale backend=2
	$(MAKE) docker_cleanup_frontend

deploy_rolling_update:
	$(MAKE) docker_setup  
	$(MAKE) docker_prod_up  
	$(MAKE) docker_db_restore  
	@echo -e "\033[32m[INFO] Rolling Update concluído!\033[0m"

