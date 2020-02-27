test:
	docker-compose exec users pytest "project/tests"
shell:
	docker-compose exec users flask shell
shell-db:
	docker-compose exec users-db psql -U postgres
black:
	docker-compose exec users black project
black-check:
	docker-compose exec users black project --check
