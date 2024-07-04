TAG := "latest"
ENV := "dev"
build:
	docker build --platform linux/amd64 -t nihrd-ebr-dev-rddi-glue-job-router:${TAG} .
	docker tag nihrd-ebr-rddi-glue-dev-job-router:${TAG} 462580661309.dkr.ecr.eu-west-2.amazonaws.com/nihrd-ecr-${ENV}-rddi-glue-job-router:${TAG}
push:
	docker push 462580661309.dkr.ecr.eu-west-2.amazonaws.com/nihrd-ecr-${ENV}-rddi-glue-job-router:${TAG}
run:
	docker run -e TARGET_BUCKET=${TARGET_BUCKET} -e AWS_SESSION_TOKEN=${AWS_SESSION_TOKEN} -e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} -e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} -p 9000:8080 462580661309.dkr.ecr.eu-west-2.amazonaws.com/nihrd-ecr-${ENV}-rddi-glue-job-router:${TAG}
	