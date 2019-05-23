# Postcodes


## Introduction

This project celebrates a list of stores and their geographical data.  There are two main functions of this project:

* To list our stores alongside their postcodes and coordinates.
* To search for stores within a radius of any UK postcode.

Based upon the Django framework, and utilises postodes.io for their UK postcode and geodata database.

## Prerequisites

* Python3

## Development 

To build this project locally, set up and activate your virtual environment.

```
python3 -m venv pyenv
source pyenv/bin/activate
```

Install dependencies.

```
pip install -r requirements.txt
```

Run database migrations.

```
python manage.py migrate
```

Finally, run the server.

```
python manage.py runserver
```

The project will now be available at `http://localhost:8000`.

## Useage

* `http://localhost:8000` will list our stores alongside their geographical data.
* `http://localhost:8000/radius/<postcode>/<radius>` will list all stores within a given radius, where -
    * `<postcode>` is any valid UK postcode, for example, SW1A 1AA.
    * `<radius>` is the radius, or distance, in which you'd like to search for stores in km. For example, 100.


## Testing

To run tests, execute the following from within your virtual environment:

```
python manage.py test
```

## Linting

To lint the project (we use [PEP8](https://www.python.org/dev/peps/pep-0008/)), run the following from within your virtual environment:

```
flake8
```

## Credits

As always, thank you to [Django](https://www.djangoproject.com/) for allowing me to prototype so quickly. Thank you also to my kettle, which has provided many cups of tea throughout this project.



