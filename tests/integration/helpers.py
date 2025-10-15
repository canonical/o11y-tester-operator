import os
import shlex
import shutil
import subprocess
from contextlib import contextmanager
import jubilant


@contextmanager
def chdir(path):
    old = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(old)


class TfDirManager:
    def __init__(self, base_tmpdir):
        self.base = str(base_tmpdir)
        self.dirs = {}  # tf_file -> path (string)

    def init(self, tf_file: str):
        name = tf_file.split(".tf")[0]
        tf_dir = os.path.join(self.base, "terraform", name)
        os.makedirs(tf_dir, exist_ok=True)
        shutil.copy(tf_file, tf_dir)

        with chdir(tf_dir):
            subprocess.run(shlex.split("terraform init"), check=True)

        self.dirs[tf_file] = tf_dir

    def apply(self, tf_file: str, juju: jubilant.Juju, **kwargs):
        kwargs = {"model": juju.model, **kwargs}
        var_str = " ".join(f"-var {k}={v}" for k, v in kwargs.items())
        cmd_str = "terraform apply -auto-approve " + var_str

        with chdir(str(self.dirs[tf_file])):
            subprocess.run(shlex.split(cmd_str), check=True)

        print("\nwaiting for the model to settle ...\n")
        juju.wait(jubilant.all_agents_idle, delay=5, timeout=60 * 10)

    def get(self, name: str):
        return self.dirs[name]





def terraform_destroy(juju: jubilant.Juju, tf_dir: str, **kwargs):
    kwargs = {"model": juju.model, **kwargs}
    var_chunk = " ".join(f"-var {k}={v}" for k, v in kwargs.items())
    cmd_str = "terraform apply -auto-approve " + " " + var_chunk

    with chdir(str(tf_dir)):
        subprocess.run(shlex.split(cmd_str), check=True)
