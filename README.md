# MosaicPay-backend
Bringing together different elements of fintech, such as accounts, transactions, and documents, to provide comprehensive payment solutions.
<br>

<details>
	<summary><b>SETTING UP MosaicPay</b></summary>
<br>

Download the project files on this [link](https://github.com/HarisKordic/MosaicPay-backend/tree/dev)

Setup the .env file **in the root of the mosaicpay** project for the backend service MosaicPay-Backend/mosaicpay. Setup the .env.development file in **the root of the frontend** folder for the Next.js application MosaicPay-Backend/mosaicpay/frontend.



**Navigate to the root folder MosaicPay-Backend/mosaicpay and run the following command**

<code>docker compose up --build </code>

Wait for the services and containers to load and go live. 



**API TESTING**	

You can test the API endpoints via Swagger on this [link](http://localhost:8000/swagger/). **Be careful to run the docker compose command before accessing Swagger**

**APP TESTING**

App [link](http://localhost:3000/login)

The app is fully functional from the base start. Dummy logins and accounts are:

​      "email": "johndoe@example.com",

​      "password": "password123"

​      "email": "janesmith@example.com",

​      "password": "qwerty456"

​      "email": "michael@example.com",

​      "password": "abcdef123"

​      "email": "emily@example.com",

​      "password": "p@ssw0rd"

​      "email": "david@example.com",

​      "password": "secret123"

Choose one of them and login. Feel free to explore the app. Create accounts, transactions, delete, edit and upload documents.



**KAFKA UI**

[Link](http://localhost:8080/)

Here you can see the different producers and events triggered in Kafka. You can also see different partitions and serialized message data.



**PG ADMIN**



You can use the [Postgre SQL DBMS](http://localhost:5050/browser/)

The master **password is codecta all lower case.**



Happy testing.

</details>

## Conventions

### General conventions:
- everything in **English**
- indentation: **4 spaces**, not tabs
- max line length: **80**
- comments/documentation max line length: **70**
---
### Naming conventions:
- function/method names are **verbs**
- boolean variables starts with **isX** or **hasX**
- pronounceable names (**addUser**, not addUsr)
- explain ambiguous name or abbreviation in a comment above the name
- comments **above** the variable/method
- flag comments (could be put in the line other than directly above variable/method) without a message:
	- ***TODO***
	- ***FIXME***
- flag comments with a message:
	- ***TODO: message***
	- ***FIXME: message***
- comments **only** when use case not understandable from variable/method name
	- // this is a comment
	- //this ain't a comment
- multiline comments like:
	- // first line
	- // second line
	- why:
		- /* */ - comments are reserved for "doc comments"
- [Allman Parentheses](https://en.wikipedia.org/wiki/Indentation_style#Allman_style) for everything (loops, conditionals, try/catch...)
- **classes** in PascalCase
- **components** in PascalCase
- **constants** in UPPER_CASE
- everything other in **camelCase**
- private **_fields**
- file names in **snake_case**
---

### Git conventions:
- commit messages in **imperative**
- commit messages starting with a **lowercase** letter
- [commit message standars](https://gist.github.com/tonibardina/9290fbc7d605b4f86919426e614fe692)
- linking **"AB#nn"** in a **new line** in a commit message
- **no** commit message ends with a period, question or exclamation mark
- workflow: [*gitflow*](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)
---

### Database conventions:
- table names using **snake_case**; lowercase
- column names using **snake_case**; lowercase

---
