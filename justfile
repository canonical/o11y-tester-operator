set export  # Just variables are exported to environment variable

[working-directory("./tests/integration/cos")]
upgrade-cos *args='':
  echo "Executing cos ... ${args}"

[working-directory("./tests/integration/cos-lite")]
upgrade-cos-lite *args='':
  echo "Executing cos-lite ... ${args}"
  uv run pytest -vvs "${args}"
