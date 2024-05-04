# csb-project1
University of Helsinki's Cyber Security Base course project I

Working and secure software and setup will be found from `main` branch and all the flaws does have their own branches.

### Installation 

Clone repository, open working directory and activate python virtual environment with:

```bash
git clone https://github.com/Pekk4/csb-project1
cd csb-project1/
python3 -m venv venv
```

Then install project's dependencies:

```bash
pip install -r requirements.txt
```

Next run Django's migrations and then you can start the server:

```bash
cd project/
python3 manage.py migrate
python3 manage.py runserver
```

Attacker server in attacker/ works with the same virtualenv, so activate it in another terminal and then start it in the same way.

If you want to use pre-configured users, run 

```bash
python3 manage.py loaddata users.json
```

before starting the server. It contains following users:

```
dumbledore:*l-~Phi=y,e^s.!x9Tio (Administrator account)
bob:dylan666
alice:cooper666
testuser1 (for testing deleting functionality)
testuser2 (for testing deleting functionality)
testuser3 (for testing deleting functionality)
```
