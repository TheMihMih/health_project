setup:
	pip install -r requirements.txt

run: setup
	python3 create_db.py
	python3 create_admin.py

clean:
	rm -rf __pycache__

docker_build:
	docker build -t health

docker_run:
	docker run --rm --name project -p 5000:5000 health