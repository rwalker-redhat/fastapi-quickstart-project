# fastapi-quickstart-project

## RHEL8

Clone this repository:

```shell
git clone https://github.com/rwalker-redhat/fastapi-quickstart-project.git
```

Change into the project directory:

```shell
cd fastapi-quickstart-project
```

Install Python 3.x

```shell
dnf module enable python39
```

```shell
dnf install python3.9
```

Create a Python Virtual Environment:

```shell
python3.9 -m venv venv
````

Activate and install requirements:

```shell
. venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt 
```

Run application:

```shell
python main.py
```