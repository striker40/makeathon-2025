#!/usr/bin/env python3
import os
import sys
import venv
import subprocess
import shutil

# RUN WITH python venv_manager.py make OR python venv_manager.py clean

VENV_DIR = "venv"
REQUIREMENTS_FILE = "requirements.txt"

def make_venv():
    if os.path.exists(VENV_DIR):
        print(f"Virtual environment '{VENV_DIR}' already exists.")
        return
    
    print("Creating virtual environment...")
    venv.create(VENV_DIR, with_pip=True)
    
    # Determine the correct pip path based on OS
    pip_path = os.path.join(VENV_DIR, "Scripts", "pip") if sys.platform == "win32" else os.path.join(VENV_DIR, "bin", "pip")
    
    print("Upgrading pip...")
    subprocess.run([pip_path, "install", "--upgrade", "pip"])
    
    if os.path.exists(REQUIREMENTS_FILE):
        print(f"Installing requirements from {REQUIREMENTS_FILE}...")
        subprocess.run([pip_path, "install", "-r", REQUIREMENTS_FILE])
    else:
        print(f"{REQUIREMENTS_FILE} not found. Skipping requirements installation.")

def clean_venv():
    if os.path.exists(VENV_DIR):
        print(f"Removing virtual environment '{VENV_DIR}'...")
        shutil.rmtree(VENV_DIR)
    else:
        print(f"Virtual environment '{VENV_DIR}' does not exist.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python venv_manager.py [make|clean]")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    if command == "make":
        make_venv()
    elif command == "clean":
        clean_venv()
    else:
        print("Invalid command. Usage: python venv_manager.py [make|clean]")
        sys.exit(1)
