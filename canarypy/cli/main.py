import click
import os
from canarypy.services.product import ProductService
from canarypy.services.release import ReleaseService
from canarypy.services.signal import SignalService
from PyInquirer import prompt


@click.group()
def cli():
    pass


@cli.group()
def product():
    pass


@product.command()
def create():
    product_service = ProductService(base_url=os.getenv('CANARYPY_URL'))

    product_create_questions = [
        {
            'type': 'input',
            'name': 'description',
            'message': 'Enter a brief description of this product?'
        },
        {
            'type': 'input',
            'name': 'repository_url',
            'message': 'What the git repository url of this product?'
        },
        {
            'type': 'input',
            'name': 'artifact_url',
            'message': 'What the artifact url of this product?'
        }
    ]
    project_answers = prompt(product_create_questions)

    response = product_service.add_product(product=project_answers)
    print(response.text)


@cli.group()
def release():
    pass


@release.command()
@click.option('--semver_version')
@click.option('--artifact_url')
def create(artifact_url, semver_version):
    release_service = ReleaseService(base_url=os.getenv('CANARYPY_URL'))
    response = release_service.add_release(release={
        'artifact_url': artifact_url,
        'semver_version': semver_version
    })
    print(response.text)


@cli.group()
def signal():
    pass


@signal.command()
@click.option('--status')
@click.option('--description')
@click.option('--instance_id')
@click.option('--semver_version')
@click.option('--artifact_url')
def create(artifact_url, semver_version, instance_id, description, status):
    release_service = SignalService(base_url=os.getenv('CANARYPY_URL'))
    response = release_service.add_signal(signal={
        'artifact_url': artifact_url,
        'semver_version': semver_version,
        'instance_id': instance_id,
        'description': description,
        'status': status
    })
    print(response.text)
