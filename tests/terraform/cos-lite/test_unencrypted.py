import jubilant
import pytest

CHANNEL = "1/stable"
COS_TF_FILE = "cos-lite.tf"


@pytest.mark.abort_on_fail
def test_deploy_cos(tf_manager, cos_model: jubilant.Juju):
    # GIVEN an initialized COS Lite TF module
    tf_manager.init(COS_TF_FILE)

    # WHEN COS Lite is deployed unencrypted
    tf_manager.apply(
        COS_TF_FILE,
        cos_model,
        channel=CHANNEL,
        internal_tls="false",
    )
    # THEN the model is active/idle
