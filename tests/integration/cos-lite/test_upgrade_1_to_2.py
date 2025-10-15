import jubilant
import pytest
from helpers import terraform_init, terraform_deploy, terraform_destroy, terraform_upgrade


@pytest.mark.abort_on_fail
def test_deploy(tmpdir, juju: jubilant.Juju):
    terraform_init(tmpdir)
    print("This is running custom track 1 code")


# @pytest.mark.abort_on_fail
# def test_upgrade(juju: jubilant.Juju):
#     terraform_upgrade(juju, "2/edge")


# @pytest.mark.abort_on_fail
# @pytest.mark.skip(
#     reason='Traefik hits error state on destroying the model due to hook failed: "receive-ca-cert-relation-broken"'
# )
# def test_destroy(juju: jubilant.Juju):
#     pass
#     # from helpers import terraform_destroy
#     # terraform_destroy(juju, "2/edge")
