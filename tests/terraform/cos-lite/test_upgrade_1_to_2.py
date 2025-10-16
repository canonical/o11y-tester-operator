import jubilant
import pytest

COS_TF_FILE = "cos-lite.tf"


# TODO: The difference is that the justfile passes the reldir in, e.g. tests/integration/cos-lite, whereas pytest is run from root.
# Also, the tests/integration folder is run automatically so I could either rename it to someone not automatically picked up or make it tox compatible
# FYI, I need to be able to spawn these manually so I think custom workflows are needed, :. a new dir name is likely best

@pytest.mark.abort_on_fail
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
def test_destroy(tf_manager, cos_model: jubilant.Juju):
    pass
    # tf_manager.apply(COS_TF_FILE, cos_model, channel="2/edge")
