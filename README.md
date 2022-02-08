# py-lyfe

[![py-lyfe](https://github.com/galactic-filament/py-lyfe/actions/workflows/python-app.yml/badge.svg)](https://github.com/galactic-filament/py-lyfe/actions/workflows/python-app.yml)
[![Coverage Status](https://coveralls.io/repos/github/galactic-filament/py-lyfe/badge.svg?branch=master)](https://coveralls.io/github/galactic-filament/py-lyfe?branch=master)

## Libraries

| Kind                  | Name                                                  |
|-----------------------|-------------------------------------------------------|
| Web Framework         | [Flask](http://flask.pocoo.org/)                      |
| SQL ORM               | [SqlAlchemy](http://www.sqlalchemy.org/)              |
| Logging               | stdlib                                                |
| Test Framework        | [pytest](https://docs.pytest.org/en/latest/)          |
| Test Coverage         | [coverage](https://coverage.readthedocs.io/en/6.3.1/) |
| Version Management    | [pyenv](https://github.com/pyenv/pyenv)               |
| Dependency Management | [poetry](https://python-poetry.org/)                  |

## Features Implemented

- [x] Hello world routes
- [x] CRUD routes for persisting posts
- [x] Database access
- [x] Database migrations
- [x] Request logging to /srv/app/log/app.log
- [x] Proper unit tests
- [x] Unit test coverage reporting
- [x] Automated testing using GitHub Actions
- [x] Automated coverage reporting using Coveralls
- [x] CRUD routes for user management
- [x] Password encryption using bcrypt
- [x] Routes protected via Bearer token authentication
- [ ] Routes protected via ACLs
- [ ] [Forms protected by CSRF](https://flask-wtf.readthedocs.io/en/1.0.x/)
- [x] Validates environment (env vars, database host and port are accessible)
