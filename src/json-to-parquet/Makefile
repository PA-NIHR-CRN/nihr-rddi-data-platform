TAG := "latest"
ENV := "dev"
build:
	docker build --platform linux/amd64 -t nihrd-ecr-dev-rddi-raw-ingestion .
	docker tag nihrd-ecr-dev-rddi-raw-ingestion:latest 462580661309.dkr.ecr.eu-west-2.amazonaws.com/nihrd-ecr-${ENV}-rddi-raw-ingestion:${TAG}
push:
	docker push 462580661309.dkr.ecr.eu-west-2.amazonaws.com/nihrd-ecr-${ENV}-rddi-raw-ingestion:${TAG}
run:
	docker run -e TARGET_BUCKET=${TARGET_BUCKET} -e AWS_SESSION_TOKEN=${AWS_SESSION_TOKEN} -e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} -e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} -p 9000:8080 462580661309.dkr.ecr.eu-west-2.amazonaws.com/nihrd-ecr-${DEV}-rddi-raw-ingestion:${TAG}
	