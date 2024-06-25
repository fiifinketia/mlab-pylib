import os
import shutil
import subprocess
import uuid

from .utils import make_file


NATIVE_PACKAGES = ['pymlab.test', 'pymlab.train']

def load_pkg(
    p_type: str,
    name: str,
    to: str,
):
    if p_type == 'native':
        load_native_pkg(name, to)
        return
    raise Exception("Only native types allowed now")

def load_native_pkg(name: str, to: str):
    if NATIVE_PACKAGES.index(name) == -1:
        raise Exception("Selected package does not exist")
    # find the native package which is a file `name.py` in current directory
    # then create a copy of the file in the to directory
    copy_native_package(name, to)

def find_native_package(name: str) -> str:
  current_directory = os.getcwd()
  for file_name in os.listdir(current_directory):
    if file_name == f"{name}.py":
      return os.path.join(current_directory, file_name)
  raise Exception("Native package not found")

def copy_native_package(name: str, to: str):
  package_path = find_native_package(name)
  shutil.copy(package_path, to)

def run_native_pkg(
    name: str,
    at: str,
    result_id: uuid.UUID,
    api_url: str,
    user_token: str,
    venv_name: str | None =  None,
    trained_model: str | None = None,
) -> subprocess.Popen[bytes]:
    """Run a script in a virtual environment using ProcessPoolExecutor"""
    # Activate the virtual environment
    # venv_path = f"{at}/venv"
    # activate_venv = f"conda {venv_name}"

    # Prepare the command to run the script with arguments
    # script_path = f"{at}/main.py"
    config_path = f"{at}/config.txt"
    os.chdir(at)
    stderr_file_path = f"{at}/{make_file(str(result_id), 'stderr.log')}"
    stdout_file_path = f"{at}/{make_file(str(result_id), 'stdout.log')}"
    run_script = f"cog train -i config={config_path} -i result_id={result_id} -i api_url={api_url} -i pkg_name={name} -i user_token={user_token}"
    if trained_model is not None:
        run_script += f" -i trained_model={trained_model}"
    print(run_script)
    # Combine the commands

    with subprocess.Popen(run_script, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, executable="/bin/bash", cwd=at) as process:
        if process.stdout is not None and process.stderr is not None:
            with process.stdout as stdout, process.stderr as stderr:
                stderr_file = open(stderr_file_path, "wb")
                stdout_file = open(stdout_file_path, "wb")
                stderr_file.write(stderr.read())
                stdout_file.write(stdout.read())
        return process