 
install:
python -m venv venv &&
venv\Scripts\activate && pip install -r requirements.txt

test:
venv\Scripts\activate && pytest

#Testing github actions


