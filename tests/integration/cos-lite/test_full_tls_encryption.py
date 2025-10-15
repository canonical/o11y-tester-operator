import jubilant
import pytest

CHANNEL = "1/stable"
CA_TF_FILE = "ca.tf"
COS_TF_FILE = "cos-lite.tf"


@pytest.mark.abort_on_fail
def test_deploy_ca(tf_manager, ca_model: jubilant.Juju):
    tf_manager.init(CA_TF_FILE)
    tf_manager.apply(CA_TF_FILE, ca_model)


@pytest.mark.abort_on_fail
def test_deploy_cos(tf_manager, ca_model: jubilant.Juju, cos_model: jubilant.Juju):
    # GIVEN an initialized COS Lite TF module
    tf_manager.init(COS_TF_FILE)
    assert ca_model.model

    # WHEN the external CA provides COS Lite certificates
    cos_model.consume(f"{ca_model.model}.certificates")
    certificates_app = cos_model.status().app_endpoints.get("certificates")
    assert certificates_app

    # AND WHEN COS Lite is deployed in full-encryption mode (both internal and external TLS)
    tf_manager.apply(
        COS_TF_FILE,
        cos_model,
        channel=CHANNEL,
        internal_tls="true",
        external_certificates_offer_url=certificates_app.url,
    )
    # THEN the model is active/idle
