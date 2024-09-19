# Django REST Application Template
This template is used to setup the base for your Django RESTful API. It comes with the following;
- Packages
    - Python Decouple - which connects the environment variables to the application
    - Psycopg - PostgreSQL database adapter for Python
    - DRF Spectacular - Sane and flexible OpenAPI 3 schema generation for Django REST framework
- Configured settings for;
	- Environment variables - SECRET_KEY, ADMIN_SITE_URL and DEBUG
  	- Database
  	- Static files
  	- REST Framwork
  	- DRF Spectacular
- Included URLs for;
	- Home
 	- Schema
  	- Swagger Documentation

## Implementing the template
1. Click on `Use this template` and then `Create a new repository`
2. Clone your new repository into an empty directory
3. Setup your virtual environment
    - Create the virtual environment; `virtualenv <virtual environment name>`
    - Activate the environment; `source <virtual environment name>/Scripts/activate`
    - To deactivate the environment; `deactivate`
4. Add your environment variables with the following command - this will add SECRET_KEY, ADIM_SITE_URL and DEBUG in the .env file;
    ```PowerShell
    python -c "import secrets; write_to=open('./application/.env','w',encoding='utf-8'); write_to.write('SECRET_KEY={0}\nADMIN_SITE_URL={1}\nDEBUG=True\n'.format(secrets.token_urlsafe(),secrets.token_urlsafe()))"
    ```
5. Setup your Database using [pgAdmin4](https://www.postgresql.org/download/);
    - Open the application and click on Servers
    - Select a PostgreSQL server and create a database in it
    - In your .env file, create the following variables for your database - retrieve `USER`, `HOST` and `PORT` from the server properties in the **Connection** tab
        ```
        USER=your_db_user
        PASSWORD=your_password
        HOST=your_host
        PORT=your_port
        NAME=your_db_name
        ```
6. Build the application; `bash build.sh` which will install the application packages, collect static files and submit your project's default databases to the server
7. Run your application; `python manage.py runserver`
