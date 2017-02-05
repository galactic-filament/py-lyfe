import os
import sys

env_var_names = [
  'APP_PORT',
  'APP_LOG_DIR',
  'DATABASE_HOST'
]
env_vars = dict(zip(env_var_names, [os.getenv(value, None) for value in env_var_names]))
missing_env_vars = { k: v for k, v in env_vars.items() if v is None }
if len(missing_env_vars) > 0:
  for name, value in missing_env_vars.items():
    print('{0} was missing'.format(name))
  sys.exit(1)

print('ayy')