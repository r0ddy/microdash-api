# microdash-api

## Getting Started

0. Install gcloud CLI using this [link] (https://cloud.google.com/sdk/docs/install) or the following command:
   ```
   curl https://sdk.cloud.google.com | bash
   ```
1. Install postgresql
   ```
   brew install postgresql
   ```
2. Login with gcloud

   ```
   # Choose gmail that you is linked with GCP project
   gcloud auth login
   gcloud init
   # Enter project id which is django-app-346321
   # Ask Roddy for access.
   ```

3. Start virtual environment and install dependencies.

   ```
   cd microdash
   python -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. Install SQL Auth Proxy (for running db)

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

5. Run SQL Auth Proxy

   ```
   # Open new terminal window.
   sudo ./run-db-proxy
   ```

6. Run Django migrations and generate static files.

   ```
   # Go back to other terminal window now.
   export GOOGLE_CLOUD_PROJECT=django-app-346321
   export USE_CLOUD_SQL_AUTH_PROXY=true
   python manage.py makemigrations
   python manage.py makemigrations polls
   python manage.py migrate
   python manage.py collectstatic
   ```

7. Open https://localhost:8000/admin
