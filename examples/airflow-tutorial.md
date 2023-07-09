## Canarypy Airflow Tutorial

This page provides a tutorial on how to use `canarypy` with Apache Airflow. It assumes that you have a working knowledge of Airflow.

### Environment setup

1. From the root of the `examples` directory, run `docker-compose up -d` to start the `canarypy` backend. This will create the folowing containers:
* `API`: The `canarypy` backend API.
* `DB`: The `canarypy` backend database.
* `WEB`: The `canarypy` backend dashboard.
* `INIT`: Temporary container that runs the `canarypy` backend database migrations.

2. From the root of the `examples/airflow` directory, run `docker-compose up -d` to start the Airflow instance. This will create the local Airflow setup with the `canarypy` plugin package already installed.

If you can access http://localhost:8080, then the Airflow instance is running correctly. The airflow user/passwrod is: airflow/airflow.

In the Airflow DAG list, you should see a DAG called `docker_operator_demo`. This DAG contains three `DockerOperator` tasks that uses the `python` image to print basic commands. On this tutorial, we'll create a few releases to demo the version switching automatically.

### Canarypy setup

The very first thing to do within Canarypy is to create a Product. In our example is Python.

### 1. Create a product in the `canarypy` backend

The `canarypy` command-line interface (CLI) provides commands to interact with the `canarypy` backend. The `product create` command is used to create a new product.

Before running the command, we need to specify the `canarypy` backend URL by setting the `CANARYPY_URL` environment variable. This can be done directly in the command line like so:

```bash
export CANARYPY_URL=http://localhost:9090
```

This sets the backend URL to `http://localhost:9090`. Ensure that your `canarypy` backend is running on this URL. If it's running on a different URL, replace `http://localhost:9090` with the correct URL.

After setting the `CANARYPY_URL`, you can create the product:

```bash
canarypy product create
```

This command will prompt you a few questions:
* `Enter the name of this product?` super python
* `What the git repository url of this product?` https://github.com/python/cpython
* `What the artifact url of this product?` python

The artifact url is what it will be used by Canarypy Airflow plugin to fetch the correct artifact.  

### 2. Create a release for the product

The `canarypy release create` command is used to create a new release for a product. This command takes a `--semver-version` argument to specify the semantic version of the release, and an `--artifact-url` argument to specify the URL where the release's artifact can be downloaded.

In a real world scenario, the `canarypy release create` command can be integrated into your CI/CD pipeline. After your product is built and deployed, the command can be executed to create a new release in the `canarypy` backend:

```bash
canarypy release create --semver-version 3.10-bullseye --artifact-url python
```

After creating the release, trigger the DAG in the Airflow UI at `http://localhost:8080`. You can check the logs of the Docker operator to confirm that it's using the correct version.

### 5. Create another release and check the DAG running on the newest version

To create another release for your product, use the `canarypy release create` command again with the new version and artifact URL:

```bash
canarypy release create --semver-version 3.11-bullseye --artifact-url python
```

Now check that the DAG will run using the newest release version of your product.
