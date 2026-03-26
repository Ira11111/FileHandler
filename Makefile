.PHONY: $(MAKECMDGOALS)

up:
	docker compose up -d

down:
	docker compose down

test-file:
	python ./utils/

test-e2e:
	PYTHONPATH=. pytest ./test/e2e/test_file_handling.py -s