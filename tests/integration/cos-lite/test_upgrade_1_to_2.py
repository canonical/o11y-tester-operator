import jubilant
import pytest

COS_TF_FILE = "cos-lite.tf"


@pytest.mark.abort_on_fail
@pytest.mark.setup
def test_deploy(tf_manager, cos_model: jubilant.Juju):
    tf_manager.init(COS_TF_FILE)
    tf_manager.apply(COS_TF_FILE, cos_model, channel="1/stable")


@pytest.mark.abort_on_fail
def test_upgrade(tf_manager, cos_model: jubilant.Juju):
    tf_manager.apply(COS_TF_FILE, cos_model, channel="2/edge")


@pytest.mark.abort_on_fail
@pytest.mark.skip(
    reason='Traefik hits error state on destroying the model due to hook failed: "'
    'receive-ca-cert-relation-broken"'
)
def test_destroy(cos_model: jubilant.Juju):
    pass
    # from helpers import terraform_destroy
    # terraform_destroy(cos_model, channel="2/edge")
