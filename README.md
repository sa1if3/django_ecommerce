# Django Ecommerce

## Installation
### Download the project
`git clone https://github.com/sa1if3/django_ecommerce` or `[Download ZIP](https://github.com/sa1if3/django_ecommerce/archive/refs/heads/main.zip)`

### Set Environment 
Create a Virtual Environment
```bash
virtualenv venv
```

Activate Virtual Environment
```bash
source venv/bin/activate
```

Download Prequisites using requirements.txt
```bash
pip install -r requirements.txt
```

Deactivate Virtual Environment
```bash
deactivate
```

### Async Tasks using Celery and Redis
Install Redis in Ubuntu 20.04 by following this [tutorial](https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-18-04)

In `settings.py` set the following variables. Change according to your use-case.

```python
BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'
```

Activate Virtual Environment
```bash
source venv/bin/activate
```

Run Celery worker
```bash
celery -A django_ecommerce  worker -l info
```

[Note: In production this command can be put in Supervisor]