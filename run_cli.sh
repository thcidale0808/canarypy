#CANARYPY_URL=http://localhost:9090 canarypy product create
CANARYPY_URL=http://localhost:9090 canarypy release create --artifact_url python --semver_version 3.9.16
CANARYPY_URL=http://localhost:9090 canarypy signal create --artifact_url python --semver_version 3.9.16 --description airflow --status success --instance_id prod
#CANARYPY_URL=http://localhost:8080 canarypy signal create --artifact_url sdf --semver_version 0.0.1 --description airflow --status success --instance_id prod