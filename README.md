# Cyber Security Base project I
University of Helsinki's Cyber Security Base course project I

# IMPORTANT NOTE!
Adding .env file was missing from the original essay's instructions (the one submitted to course page) and it's needed to run main branch version of the application!

### Flaws
Working and secure software and setup will be found from [main](https://github.com/Pekk4/csb-project1/tree/main) branch and all the flaws does have their own branches:

 - [flaw_csrf](https://github.com/Pekk4/csb-project1/tree/flaw_csrf)
 - [flaw_injection](https://github.com/Pekk4/csb-project1/tree/flaw_injection)
 - [flaw_xss](https://github.com/Pekk4/csb-project1/tree/flaw_xss)
 - [flaw_broken_access_control](https://github.com/Pekk4/csb-project1/tree/flaw_broken_access_control)
 - [flaw_security_misconfiguration](https://github.com/Pekk4/csb-project1/tree/flaw_security_misconfiguration)

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

Next set .env file, run Django's migrations and then you can start the server:

```bash
cd project/
mv .env.example .env # Add secret key into the .env file, it can be generated e.g. by running 'openssl rand -base64 32' (without quotes)
python3 manage.py migrate
python3 manage.py runserver
```

Attacker server in attacker/ works with the same virtualenv, so activate it in another terminal and then start it in the same way.

#### Pre-configured users 
If you want to use pre-configured users (in the main app, attacker server does not need users), run 

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
