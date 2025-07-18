from setuptools import setup, find_packages

with open("requirements.txt") as f: # Read requirements from file
    requirements = f.read().splitlines() # read line by line

setup(
    name = "First-Project",
    version = "0.1.0",
    author = "Nikunjkumar Mahida",
    packages = find_packages(), # Automatically find packages in the directory
    install_requires = requirements, # Install dependencies from requirements.txt
)
