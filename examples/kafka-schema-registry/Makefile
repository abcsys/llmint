.PHONY: schema version v1
schema:
	curl -X GET http://localhost:8081/subjects
version:
	curl -X GET http://localhost:8081/subjects/user-info-value/versions
v1:
	curl -X GET http://localhost:8081/subjects/user-info-value/versions/1

.PHONY: run
run:
	python s1_register.py
	python s2_producer.py
	python s3_evolve.py
	python s4_producer_v2.py
	python s5_consumer.py
