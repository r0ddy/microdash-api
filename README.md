# microdash-api

## Getting Started

1. Start virtual environment and install dependencies.

```
cd microdash
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

2. Install SQL Auth Proxy (for running db)

```
gcloud auth application-default login
```

If using macOS (64-bit)

```
curl -o cloud_sql_proxy https://dl.google.com/cloudsql/cloud_sql_proxy.darwin.amd64
chmod +x cloud_sql_proxy
```

If using macOS (M1)

```
curl -o cloud_sql_proxy https://dl.google.com/cloudsql/cloud_sql_proxy.darwin.arm64
chmod +x cloud_sql_proxy
```

Move to home directory

```
mv cloud_sql_proxy ~/
```

3. Run SQL Auth Proxy

```
# Open new terminal window.
sudo ./run-db-proxy
```

4. Run Django migrations and generate static files.

```
# Go back to other terminal window now.
export GOOGLE_CLOUD_PROJECT=django-app-346321
export USE_CLOUD_SQL_AUTH_PROXY=true
python manage.py makemigrations
python manage.py makemigrations polls
python manage.py migrate
python manage.py collectstatic
```

5. Open https://localhost:8000/admin
