#!/usr/bin/python
try:
    from tqdm import tqdm; import os; import json; import sys; from urllib.request import urlretrieve; from datetime import datetime; import platform; from pathlib import Path; import shutil; import argparse
except:
    print("Not all dependencies have been installed!!")
    sys.exit(1)
def get_install_path(name):
    if platform.system() == "Windows":
        return Path(os.getenv("ROAMING"), "rbox", name)
    elif platform.system() == "Linux":
        return Path(Path.home(), "Applications", name)
    else:
        return Path(Path.home(), "Library", "Application Support", name)
def remove_pkg(name, skip):
    try:
        install_path = get_install_path(name)
        if not install_path.exists():
            print(f"{name} has not yet been installed!")
        if not skip:
            c = input(f"Are you sure you want to remove {name}? (Y/N): ").lower()
            if c != "y":
                print("Removal has been cancelled")
                return
        shutil.rmtree(install_path)
        print(f"Removal of {name} succecsfull")
    except Exception as e:
        print(f"Something unexpected happened while removing {name} : {str(e)}, Please try again!")
def update_pkglist():
    url = "https://raw.githubusercontent.com/eska-0/dbox/refs/heads/main/packages.json"
    try:
        try:
            with open(get_install_path("packages.json"), 'r') as r:
                data = json.load(r)
            url = data.get('updateurl')
            print("Updating packagelist.")
            urlretrieve(url, get_install_path("packages.json"))
            print("Packagelist was updated.")
        except:
            print("Package list is missing or corrupted...")
            print("Installing package list.")
            urlretrieve(url, get_install_path("packages.json"))
            print("Packagelist was installed.")
    except Exception as e:
        print(f"Failed to update or install packagelist: {e}")
def install_pkg(name, skip):
    try:
        with open(get_install_path("packages.json"), 'r') as r:
            data = json.load(r)
            pdata = data.get("packages", [])
        for i in pdata:
            if name == i("name"):
                if platform.system() in pdata["url"]:
                    URL = pdata["url"][platform.system().lower()]
                    if not skip:
                        c = input(f"Are you sure you want to install {name} to {get_install_path(name)} (Y/N): ").strip().lower()
                        if "y" == c:
                            PATH = get_install_path(name)
                            PATH.mkdir(parents=True, exist_ok=True)
                            with tqdm(total=100, desc=f"Downloading {name}", unit='%', bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}') as pbar:
                                urlretrieve(
                                     URL, PATH, 
                                    reporthook=lambda count, block_size, total_size: pbar.update(block_size / total_size * 100)
                                )
                            if PATH.exists():
                                print(f"Installation of {name} succesfull")
                                sys.exit(1)
                        else:
                            print("Installation canceled")
                            sys.exit(1)
                                                
                else:
                    print(f"This package is unavailable on {platform.system()}")
                    sys.exit(1)
        print(f"No package found with name: {name}")
        sys.exit(1)
    except Exception as e:
        print(f"Error : {e}")
def list_pkg():
    try:
        update_pkglist()
        with open(get_install_path("packages.json"), 'r') as r:
            data = json.load(r)
            print("Installable packages: ")
            for i in data.get("packages", []):
                print(f"name: {i["name"]}")
                print(f"version: {i["version"]}")
                print(f"description: {i["description"]}")
                print(f"repo:{i["repo"]} ")
    except FileNotFoundError:
        print("Package file not found, running rbox update -y might help. If not, idk what happened")
    except json.JSONDecodeError:
        print("Package file is corrupt, running dbox update -y might help. If not, i have no idea what happened")
def main():
    parser = argparse.ArgumentParser(description="eSKa-0's package manager")
    parser.add_argument("command", choices=["list", "install", "remove", "update", "help"], help="what you would like to do", nargs="?")
    parser.add_argument("package", help="Package name (required for install and remove commands)")
    parser.add_argument("-y", "--yes", action="store_true", help="Skip the confirmation process")
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)
    elif "list" == args.command:
        list_pkg()
    elif "install" == args.command:
        if not args.package:
            print("Don't forget to specify the package!")
            sys.exit(1)
        install_pkg(args.package, args.yes)
    elif "uninstall" == args.command:
        if not args.package:
            print("Don't forget to specify the package!")
            sys.exit(1)
        remove_pkg(args.package, args.yes)
    elif "update" == args.command:
        update_pkglist()
    elif "help" == args.command:
        parser.print_help

if __name__ == "__main__":
    main()