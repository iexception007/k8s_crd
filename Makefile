preinstall:
	sudo pip install -r requirements.txt


build:
	docker build -t crd_helper .

run: clear
	docker run --rm -d --name crd_helper crd_helper:latest
	docker logs -f crd_helper

clear:
	-docker rm -f crd_helper
