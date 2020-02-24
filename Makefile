test:
	docker-compose exec users pytest "project/tests"
shell:
	docker-compose exec users flask shell
