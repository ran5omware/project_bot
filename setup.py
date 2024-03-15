from setuptools import setup, find_packages

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="TRPP_project",
    description="library for static functions",
    version="0.0.1",
    package_dir={"": "src"},
    packages=find_packages(where='src'),
    install_requires=[
        'aiohttp==3.9.3',
        'aiosignal==1.3.1',
        'attrs==23.2.0',
        'disnake==2.9.1',
        'frozenlist==1.4.1',
        'idna==3.6',
        'multidict==6.0.5',
       ' pyaes==1.6.1',
        'Pyrogram==2.0.106',
        'PySocks==1.7.1',
        'python-dotenv==1.0.1',
        'yarl==1.9.4'
    ],
    author="ran5omware",
    author_email="",
    classifiers=["Programming Language :: Python :: 3"],
    python_requires=">=3.10",
    include_package_data=True
)
