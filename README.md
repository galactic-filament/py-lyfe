# py-lyfe

[![Build Status](https://travis-ci.org/galactic-filament/py-lyfe.svg?branch=master)](https://travis-ci.org/galactic-filament/py-lyfe)

## Libraries

Kind | Name
--- | ---
Web Framework | [Flask](http://flask.pocoo.org/)
SQL ORM | [SqlAlchemy](http://www.sqlalchemy.org/)
Logging | stdlib
Test Framework | [pytest](https://docs.pytest.org/en/latest/)
Test Coverage | n/a

## Features Implemented

- [x] Hello world routes
- [x] CRUD routes for persisting posts
- [x] Database access
- [x] Request logging to /srv/app/log/app.log
- [x] Unit tests
- [ ] Unit test coverage reporting
- [x] Automated testing using TravisCI
- [ ] Automated coverage reporting using Coveralls
- [ ] CRUD routes for user management
- [ ] Password encryption using bcrypt
- [ ] Routes protected via HTTP authentication
- [ ] Routes protected via ACLs
- [x] Validates environment (env vars, database host and port are accessible)
