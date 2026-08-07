# My Python Project
A clean template for starting Python DB Connection apps.

## Installation
Go to the folder containing db-util-0.1.0.tar.gz distribution and then execute the following command:
Run 'pip install db-util-0.1.0.tar.gz -r requirements.txt'

## Additional Dependencies
This project needs pymsql and cryptography libraries to connect with mysql database as documented in requirements.txt

## DB Connection
If you are running mysql locally then you can utilize it by configuring environment variables as shown below

And this project can be configured to connect to the Aiven for MySQL® database running in remote cloud environment. For more information see Aiven documentation.

Then configure the connection via environment variables before running your script:

$export DB_ENGINE=mysql
$export DB_HOST=localhost
$export DB_PORT=3306
$export DB_NAME=flask_demo
$export DB_USER=root
$export DB_PASS=your_password_here
$export TIMEOUT=10

## Environment configuration

The module reads its database settings from the current process environment variables rather than from .env files.

Example:
DB_HOST=localhost
DB_PORT=3306
DB_NAME=flask_demo
DB_USER=root
DB_PASS=your_password_here
TIMEOUT=10