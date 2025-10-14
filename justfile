set export  # Just variables are exported to environment variable
uv_flags := "--frozen --isolated --extra=dev"

[working-directory("./tests/integration/cos")]
upgrade-cos *args='':
  echo "Executing cos ... ${args}"

[working-directory("./tests/integration/cos-lite")]
upgrade-cos-lite *args='':
  echo "Executing cos-lite ... ${args}"
  pwd
  uv run $uv_flags pytest -vvs "${args}"
