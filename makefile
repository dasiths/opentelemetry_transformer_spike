start:
	-docker-compose down
	docker-compose up -d
	python3 app.py

stop:
	-docker-compose down
