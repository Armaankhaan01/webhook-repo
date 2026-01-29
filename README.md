# Dev Assessment - Webhook Receiver

Please use this repository for constructing the Flask webhook receiver.


## Setup
* Create a new virtual environment

```bash
git clone https://github.com/Armaankhaan01/webhook-repo.git
```
* change the directory
```bash
cd webhook-repo
```

* Create a new virtual environment

```bash
pip install virtualenv

virtualenv venv
```

* Activate the virtual env

```bash
source venv/bin/activate
```

* Install requirements

```bash
pip install -r requirements.txt
```

* Run the Flask application
  (In production, please use Gunicorn on Linux-based systems)

```bash
python run.py
```

* The webhook endpoint is available at:

```bash
POST http://127.0.0.1:5000/webhook/receiver
```

---

## Webhook Working Proof

The following image shows a successful GitHub webhook delivery and data being processed correctly by the Flask application.

![Webhook Working Screenshot](https://ibb.co/p6th0hYH)

This confirms:

* The webhook endpoint is reachable
* GitHub events are successfully received
* The application processes requests without errors

