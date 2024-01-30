.PHONY: clean env service

.venv/bin/python: requirements.txt
	python3.11 -m venv .venv
	.venv/bin/python -m pip install -r requirements.txt
	touch .venv/bin/python


env: .venv/bin/python


service: .venv/bin/python
	cd src && uvicorn service:app --host localhost --port 7777 --workers 6
	# cd src && gunicorn service:app -w 6 -k uvicorn.workers.UvicornWorker -b "localhost:7777" --reload 


clean:
	rm -rf .venv/
