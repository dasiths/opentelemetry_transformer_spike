start:
	-docker-compose down
	docker-compose up -d
	python app.py

stop:
	-docker-compose down
