# flask-api
Simple Python Flask to make an Rest-API (fe) and MySQL (be)

## Purpose of this repo
So I was fooling around with Python and wanted to make a Rest-API as front-end that communicates with a backend database. 
No problemo you would say? Yes, on my local network this doesn't pose any challenge but you need to consider hosting, and setting it up properly, consider security, SSL certificates and all that good stuff. Didn't want to put a SQL server on the web so looked at various modern ways of doing it without spinning up a containerized cluster. In my search for an integrated solution for my simple sandbox I came across [pythonanywhere](https://eu.pythonanywhere.com/) and it fit my needs perfectly so I'm hosting it there.

# Requirements
- Python 3.x 
- MySQL / MariaDB server
- Python-3, Python3-pip

# Installation 
- install all required libraries from the ```requirements.txt```. To do this on Linux:
```
python -m venv .
. bin/activate
pip install -r requirements.txt
```

## Backend 

You need at least this table for this to work
```
create table `rest_emp` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`name` varchar(255) NOT NULL,
`email` varchar(255) NOT NULL,
`phone` varchar(16) DEFAULT NULL,
`address` text DEFAULT NULL,
PRIMARY KEY(`id`)
);
```

## Usage
- ```python ./flask_app.py```
- Call the service using the Insomnia (or any other) Rest Client:
![Add](images/add.png?raw=true)
![List](images/list.png?raw=true)
