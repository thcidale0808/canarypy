import pytest
import json
import os
from unittest.mock import patch, Mock

from canarypy.cli.main import product, release, signal


def test_cli_create_product(runner):

    with patch('canarypy.cli.main.prompt', return_value={
        "description": "test description",
        "repository_url": "http://test-repo",
        "artifact_url": "http://test-artifact",
    }) as mock_prompt:
        with patch('requests.post', return_value=Mock(status_code=200)) as mock_post:
            os.environ["CANARYPY_URL"] = "http://test-url"
            result = runner.invoke(product, ['create'],
                                   input='My Product\nhttps://github.com/my-product\nhttps://github.com/my-product/releases/v1.0.0\n')
            mock_prompt.assert_called_once()
            mock_post.assert_called_once_with(
                url="http://test-url/product",
                data=json.dumps({
                    "description": "test description",
                    "repository_url": "http://test-repo",
                    "artifact_url": "http://test-artifact",
                })
            )
    assert result.exit_code == 0


def test_cli_create_release(runner):

    with patch('requests.post', return_value=Mock(status_code=200)) as mock_post:
        os.environ["CANARYPY_URL"] = "http://test-url"
        result = runner.invoke(release, ['create', '--artifact_url', 'http://test-artifact', '--semver_version', '1.0.0'])
        assert result.exit_code == 0
        mock_post.assert_called_once_with(
            url="http://test-url/release",
            data=json.dumps({
                "artifact_url": 'http://test-artifact',
                "semver_version": '1.0.0',
            })
        )
    assert result.exit_code == 0


def test_cli_create_signal(runner):
    os.environ["CANARYPY_URL"] = "http://test-url"

    with patch('requests.post', return_value=Mock(status_code=200, text='Signal created.')) as mock_post:
        result = runner.invoke(signal.commands['create'], [
            '--artifact_url', 'http://test-artifact',
            '--semver_version', '1.0.0',
            '--instance_id', 'test-instance',
            '--description', 'test-description',
            '--status', 'test-status'
        ])
        assert result.exit_code == 0
        mock_post.assert_called_once_with(
            url="http://test-url/signal",
            data=json.dumps({
                "artifact_url": 'http://test-artifact',
                "semver_version": '1.0.0',
                "instance_id": 'test-instance',
                "description": 'test-description',
                "status": 'test-status',
            })
        )
