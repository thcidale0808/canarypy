#CANARYPY_URL=http://localhost:8080 canarypy product create
#CANARYPY_URL=http://localhost:8080 canarypy release create --artifact_url sdf --semver_version 0.0.1
#CANARYPY_URL=http://localhost:8080 canarypy signal create --artifact_url sdf --semver_version 0.0.1 --description airflow --status success --instance_id prod
CANARYPY_URL=http://localhost:8080 canarypy signal create --artifact_url sdf --semver_version 0.0.1 --description airflow --status success --instance_id prod