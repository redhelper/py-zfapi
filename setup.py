import os

from setuptools import find_packages, setup

SETUP_DIRNAME = os.path.dirname(__file__)
REQ_FILE = os.path.join(
    os.path.abspath(SETUP_DIRNAME),
    "requirements.txt",
)
REQUIREMENTS = []
DEPENDENCIES = []
with open(REQ_FILE, "r") as fd:
    for line in fd.readlines():
        if not line or line.startswith("#"):
            continue
        if line.startswith("-e"):
            REQUIREMENTS.append(line.split("egg=")[1].strip())
            DEPENDENCIES.append(line[3:])
        else:
            REQUIREMENTS.append(line.split(" ")[0].strip())
setup(
    name="py-zfapi",
    version="1.0.0",
    description="ZeroFOX ZF API Wrapper",
    url="https://github.com/riskive/py-zfapi",
    author="rcalvo",
    author_email="rcalvo@zerofox.com",
    packages=find_packages(
        exclude=[
            "tests",
        ]
    ),
    install_requires=REQUIREMENTS,
    dependency_links=DEPENDENCIES,
)
