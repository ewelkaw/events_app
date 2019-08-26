# EventsApp
App for scraping chosen websites using python and then presenting data to the user using Flask and SQLite database.

## To run app we should use Makefile:
- dockerized: 
	- make build
	- make run  
- locally:
	- make run_dev
	
## To run tests we can use:
- unittest, example:
	- `python -m unittest -v tests/test_app/test_app.py`
- pytest, example:
	- `python -m pytest tests/test_data_scrapping/`

