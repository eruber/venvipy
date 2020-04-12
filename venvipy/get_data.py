# -*- coding: utf-8 -*-
"""
This module provides all the necessary data.
"""
from subprocess import Popen, PIPE
from dataclasses import dataclass
import xmlrpc.client
import shutil
import os



#]===========================================================================[#
#] FIND PYTHON 3 INSTALLATIONS [#============================================[#
#]===========================================================================[#

@dataclass
class PythonInfo:
    """_"""
    py_version: str
    py_path: str


def get_python_installs():
    """
    Get the available python versions installed.
    """
    versions = ["3.9", "3.8", "3.7", "3.6", "3.5", "3.4", "3.3"]
    py_info_list = []

    for i, version in enumerate(versions):
        python_path = shutil.which(f"python{version}")

        if python_path is not None:
            res = Popen(
                    [python_path, "-V"],
                    stdout=PIPE,
                    text="utf-8"
                )
            out, _ = res.communicate()
            python_version = out.strip()

            py_info = PythonInfo(python_version, python_path)
            py_info_list.append(py_info)

    return py_info_list


#]===========================================================================[#
#] GET VENVS [#==============================================================[#
#]===========================================================================[#

@dataclass
class VenvInfo:
    """_"""
    venv_name: str
    venv_version: str


def get_venvs(path):
    """
    Get the available virtual environments
    from the specified folder.
    """
    # return an emtpty list if directory doesn't exist
    if not os.path.isdir(path):
        return []

    venv_info_list = []

    for i, venv in enumerate(os.listdir(path)):
        # build path to venv directory
        valid_venv = os.path.join(path, venv)
        if not os.path.isdir(valid_venv):
            continue

        # build path to pyvenv.cfg file
        cfg_file = os.path.join(valid_venv, "pyvenv.cfg")
        if not os.path.isfile(cfg_file):
            continue

        version_found = get_python_vers(cfg_file)

        venv_info = VenvInfo(os.path.basename(valid_venv), version_found)
        venv_info_list.append(venv_info)

    return venv_info_list


def get_python_vers(pyvenv_cfg):
    """
    Get the Python version of a virtual environment by
    reading the version str from it's `pyvenv.cfg` file.
    """
    with open(pyvenv_cfg, "r") as f:
        lines = f.readlines()

    return f"Python {lines[2][10:]}".strip()


def get_active_dir_str():
    """
    Get the default venv directory string from `resources/default` file.
    """
    current_dir = os.path.dirname(os.path.realpath(__file__))
    default_file = os.path.join(current_dir, "resources", "default")

    if os.path.isfile(default_file):
        with open(default_file, "r") as f:
            active_dir = f.read()
            return active_dir
    else:
        with open(default_file, "w") as f:
            active_dir = f.write("")
            return active_dir

    return []


def get_active_dir():
    """
    Get the active venv directory string from file and
    pass it to `get_venvs()`.
    """
    active_dir = get_active_dir_str()
    return get_venvs(active_dir)


#]===========================================================================[#
#] GET INFOS FROM PYTHON PACKAGE INDEX [#====================================[#
#]===========================================================================[#

@dataclass
class ModuleInfo:
    """_"""
    mod_name: str
    mod_version: str
    mod_summary: str


def get_module_infos(name):
    """
    Get module name, version and description from https://pypi.org/pypi.
    """
    client = xmlrpc.client.ServerProxy("https://pypi.org/pypi")
    search_result = client.search({"name": name})

    module_info_list = []

    for i, mod in enumerate(search_result):
        mod_name = mod["name"]
        mod_version = mod["version"]
        mod_summary = mod["summary"]

        mod_info = ModuleInfo(mod_name, mod_version, mod_summary)
        module_info_list.append(mod_info)

    return module_info_list



if __name__ == "__main__":
    pass

    #for python in get_python_installs():
        #print(python.py_version, python.py_path)

    #]=======================================================================[#

    # venv in get_active_dir():
        #print(venv.name, venv.version)

    #]=======================================================================[#

    #test_module = "test"

    #for item in get_module_infos(test_mod):
        #print(item.mod_name, item.mod_version, item.mod_summary)

    #if not get_module_infos(test_module):
        #print("No modules found!")

    #print(get_active_dir())