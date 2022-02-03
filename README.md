# py-lyfe

[Build Status](#)
[![Coverage Status](https://coveralls.io/repos/github/galactic-filament/py-lyfe/badge.svg?branch=master)](https://coveralls.io/github/galactic-filament/py-lyfe?branch=master)

## Libraries

| Kind                  | Name                                                           |
|-----------------------|----------------------------------------------------------------|
| Web Framework         | [Flask](http://flask.pocoo.org/)                               |
| SQL ORM               | [SqlAlchemy](http://www.sqlalchemy.org/)                       |
| Logging               | stdlib                                                         |
| Test Framework        | [pytest](https://docs.pytest.org/en/latest/)                   |
| Test Coverage         | [pytest-coverage](http://pytest-cov.readthedocs.io/en/latest/) |
| Version Management    | [pyenv](https://github.com/pyenv/pyenv)                        |
| Dependency Management | [pipenv](https://github.com/pypa/pipenv)                       |

## Features Implemented

- [x] Hello world routes
- [x] CRUD routes for persisting posts
- [x] Database access
- [x] Request logging to /srv/app/log/app.log
- [ ] Proper unit tests
- [x] Unit test coverage reporting
- [ ] Automated testing using GitHub Actions
- [x] Automated coverage reporting using Coveralls
- [ ] CRUD routes for user management
- [ ] Password encryption using bcrypt
- [ ] Routes protected via Bearer token authentication
- [ ] Routes protected via ACLs
- [ ] Forms protected by CSRF
- [x] Validates environment (env vars, database host and port are accessible)
