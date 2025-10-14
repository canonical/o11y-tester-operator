import os
import shlex
import shutil
import subprocess

import jubilant


def terraform_init(tmpdir):
    temp_tf_dir = tmpdir.mkdir("terraform")
    shutil.copy("main.tf", temp_tf_dir)
    os.chdir(temp_tf_dir)
    subprocess.run(shlex.split(("terraform init")))


def terraform_deploy(juju: jubilant.Juju, channel: str):
    subprocess.run(
        shlex.split(
            (f"terraform apply -var model={juju.model} -var channel={channel} -auto-approve")
        )
    )
    print("\nwaiting for the model to settle ...\n")
    juju.wait(jubilant.all_agents_idle, delay=5, timeout=60 * 10)


def terraform_upgrade(juju: jubilant.Juju, channel: str):
    subprocess.run(
        shlex.split((f"terraform apply -var model={juju.model} -var channel={channel} -auto-approve"))
    )
    print("\nwaiting for the model to settle ...\n")
    juju.wait(jubilant.all_agents_idle, delay=5, timeout=60 * 10)


def terraform_destroy(juju: jubilant.Juju, channel: str):
    subprocess.run(
        shlex.split(
            (f"terraform destroy -var model={juju.model} -var channel={channel} -auto-approve")
        )
    )
