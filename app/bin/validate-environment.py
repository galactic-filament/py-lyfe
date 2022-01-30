import os
import sys
import socket

# validating that env vars are available
env_var_names = ["APP_PORT", "APP_LOG_DIR", "DATABASE_HOST"]
env_vars = dict(zip(env_var_names, [os.getenv(value, None) for value in env_var_names]))
missing_env_vars = {k: v for k, v in env_vars.items() if v is None}
if len(missing_env_vars) > 0:
    for name, value in missing_env_vars.items():
        print("{0} was missing".format(name))

    sys.exit(1)

# validating that the database port is accessible
s = socket.socket()
db_port = 5432
try:
    s.connect((env_vars["DATABASE_HOST"], db_port))
except socket.gaierror as e:
    print("Host {0} could not be found".format(env_vars["DATABASE_HOST"]))

    sys.exit(1)
except ConnectionRefusedError as e:
    print("{0} was not accessible at {1}".format(env_vars["DATABASE_HOST"], db_port))

    sys.exit(1)

# validating that the log dir exists
if os.path.exists(env_vars["APP_LOG_DIR"]) == False:
    print("{0} log dir does not exist".format(env_vars["APP_LOG_DIR"]))

    sys.exit(1)

sys.exit(0)
