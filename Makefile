CONTAINER_NAME = intra_container

all:
	docker build -t ljarrahd .
	docker run -p 80:80 -p 443:443 -d --name $(CONTAINER_NAME) ljarrahd

re: remove all

run:
	docker run -p 80:80 -p 443:443 -d --name $(CONTAINER_NAME) ljarrahd

build:
	docker build -t ljarrahd .

stop:
	docker stop $(CONTAINER_NAME)

remove:
	docker rm -f $(CONTAINER_NAME)

logs:
	docker logs $(CONTAINER_NAME)