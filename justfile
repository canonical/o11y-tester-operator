set export  # Just variables are exported to environment variable
uv_flags := "--frozen --isolated --extra=dev"

[working-directory("./tests/terraform/cos")]
test-cos *args='':
  echo "Executing cos ... ${args}"

[working-directory("./tests/terraform/cos-lite")]
test-cos-lite *args='':
  uv run $uv_flags pytest -vvs "${args}"
