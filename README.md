## Fast Frappe

FastAPI using Frappe Framework

Use example to build serverless function using frappe framework.

### Prerequisites

- Core development happens with standard `bench start`.
- Already running `frappe-bench` like setup.
- Connection to same mariadb, redis that the `frappe-bench` connects to.
- Access to `sites` directory of the `frappe-bench`
- Valid site to set it as `SITE_NAME` environment variable.
- You will also need the latest version of https://github.com/go-prime/restaurant.
- Use the branch restaurant-pos-prod

### Installation

Install as python app in frappe-bench python `env`

```shell
cd ~/frappe-bench
git clone https://github.com/castlecraft/fast_frappe apps/fast_frappe
./env/bin/pip install -e apps/fast_frappe
```

### Serve

Using `uvicorn`

```shell
cd ~/frappe-bench
. ./env/bin/activate

# Execute app from sites directory
cd ~/frappe-bench/sites
# Set SITE_NAME to use for the function
SITE_NAME=function.local uvicorn fast_frappe.main:app --port 3000
```

### Check Response

```
curl -s http://localhost:3000 | jq .
```

### Project Structure

fast_frappe/
├── __init__.py
├── config/
├── controllers/ # endpoints imported from this folder
├── ctrl.py
├── fast_frappe/
├── hooks.py
├── main.py # We will import routes into the main app here
├── modules.txt
├── patches.txt
├── serializers/ Houses our serializers for validation
└── templates/

## Work Flow
All the queries to be done in restaurant app in functions place in restaurant/apps/restaurant/restaurant/public_api.py
These functions will be called in this application from controllers folder

### Containerized

Build

```shell
cd ~/frappe-bench/apps/fast_frappe
docker build -t fast_frappe:latest .
```

Run

```shell
docker run -v /path/to/sites:/home/frappe/frappe-bench/sites --publish 3000:3000 fast_frappe:latest
```

### Description

The app consists of 2 files:

`main.py`:

```python
import frappe
from typing import Optional

from fastapi import FastAPI
from fast_frappe.ctrl import init_frappe, destroy_frappe

app = FastAPI()


@app.get("/")
def read_root():
    init_frappe()
    available_doctypes = frappe.get_list("DocType")
    settings = frappe.get_single("System Settings")
    destroy_frappe()
    return {
        "available_doctypes": available_doctypes,
        "settings": settings.as_dict(),
    }
```

and `ctrl.py`:

```python
import os

import frappe


def init_frappe():
    site = os.environ.get("SITE_NAME", "test.localhost")
    frappe.init(site=site)
    frappe.connect()


def destroy_frappe():
    frappe.destroy()
```
### License

MIT
