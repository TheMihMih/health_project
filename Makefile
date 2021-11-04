setup:
	pip install -r requirements.txt

run: setup
	python3 create_db.py
	python3 create_admin.py

clean:
	rm -rf __pycache__
