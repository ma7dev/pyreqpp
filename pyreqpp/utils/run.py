import os
import random
import shutil
import string
import subprocess
import tempfile

def run_cmd(cmd_str):
    subprocess.call(cmd_str.split(" "))


def install_dep(venv_dir, requirements_path):
    with open(requirements_path, "r") as f:
        for line in f.readlines():
            line = line.split()[0]
            subprocess.call(
                f"{venv_dir}/bin/python -m poetry add {line}".split(" ")
            )


def remove_unwanted_python_versioning(tmp_dir):
    with open(f"{tmp_dir}/with_dep_requirements.txt", "w") as fw:
        with open(f"{tmp_dir}/long_requirements.txt", "r") as f:
            for line in f.readlines():
                line = line.split(";")[0].split()[0]
                fw.write(f"{line}\n")


def remove_unwanted_dep(requirements_path, tmp_dir):
    lines = []
    with open(requirements_path, "r") as fr:
        for line in fr.readlines():
            targeted_package_name = line.split()[0].split("==")[0]
            with open(f"{tmp_dir}/with_dep_requirements.txt", "r") as f:
                for line_tmp in f.readlines():
                    tmp_package_name = line_tmp.split()[0].split("==")[0]
                    if targeted_package_name == tmp_package_name:
                        lines.append(line_tmp.split()[0])
    with open(requirements_path, "w") as f:
        for line in lines:
            f.write(f"{line}\n")


def copy_pyproject(tmp_dir):
    pyproject_sample = """
[tool.poetry]
name = "env_test"
version = "0.1.0"
description = ""
authors = ["Your Name <you@example.com>"]

[tool.poetry.dependencies]
python = "3.8.13"

[tool.poetry.dev-dependencies]

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
    """
    with open(f"{tmp_dir}/pyproject.toml", "w") as f:
        f.writelines(pyproject_sample)


def run(requirements_path, verbose=False):
    # project_dir = os.getcwd()
    random_str = f"__{''.join(random.choice(string.ascii_lowercase) for i in range(10))}"

    # create a tmp_dir
    tmp_dir = os.path.join(tempfile.gettempdir(), random_str)
    if not os.path.isdir(tmp_dir):
        os.mkdir(tmp_dir)
    else:
        raise NotImplementedError
    if verbose:
        print(tmp_dir)

    venv_dir = os.path.join(tmp_dir, ".venv")

    os.chdir(tmp_dir)
    run_cmd(f"python -m venv {venv_dir}")
    run_cmd(f"{venv_dir}/bin/python -m pip install poetry")
    copy_pyproject(tmp_dir)
    install_dep(venv_dir, requirements_path)
    run_cmd(
        f"poetry export -f requirements.txt --output long_requirements.txt --without-hashes"
    )
    remove_unwanted_python_versioning(tmp_dir)
    remove_unwanted_dep(requirements_path, tmp_dir)

    try:
        shutil.rmtree(tmp_dir)
        print(f"Removed: {tmp_dir}")
    except OSError as e:
        print(f"Error: {tmp_dir} : {e.strerror}")


def check(requirements_path, verbose=False):
    is_good_candidate = False
    with open(requirements_path, "r") as f:
        for line in f.readlines():
            if "==" not in line:
                is_good_candidate = True
                break
    if is_good_candidate:
        print("Running PyReqPP")
        run(requirements_path, verbose)
    else:
        print("No need to run PyReqPP")