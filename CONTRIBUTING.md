# Contributing to CanaryPy

We truly appreciate your interest in contributing to CanaryPy! This is an open-source project that thrives on community input and collaboration. CanaryPy offers a novel solution to handle canary releases for your data pipelines, allowing a safer and more controlled deployment of new features or updates.

## Code of Conduct

We maintain a strict code of conduct to ensure that our community remains open, welcoming, and respectful to everyone. We request all contributors to adhere to the principles outlined in the code of conduct, promoting an inclusive and healthy environment. You can find our Code of Conduct in the repository.

## Ways to Contribute

There are many ways you can contribute to CanaryPy, including but not limited to:

- **Bug Reports**: If you find a bug, please feel free to open an issue in our GitHub repository, describing the problem and how it can be reproduced.

- **Feature Requests**: If you believe that a particular feature is missing or could be improved, please open an issue providing a clear and detailed explanation of your idea.

- **Code**: Feel free to take on open issues, even those not assigned to you. When your code is ready, submit a pull request for the team to review. 

- **Documentation**: If you think our documentation could be improved, whether it's the README, inline code comments, or user guides, we would love your help.

- **Test Coverage**: Improving test coverage is a constant need. If you're comfortable writing tests, your help would be much appreciated.

## Setting Up Your Environment

Before you begin contributing, you'll need to set up a local development environment. Here's how to do it:

1. **Fork the Repository**: Start by forking the CanaryPy repository to your own GitHub account. This creates a copy of the repository that you have full control over.

2. **Clone the Repository**: Once you've forked the repository, clone it to your local machine. This creates a local copy of the project that you can edit.

3. **Set up the Environment Variables**: The CLI uses the FastAPI application as the backend. So, you need to set up the following environment variables: `CANARYPY_URL` (default: `http://localhost:8080`).

4. **Install Dependencies**: Install all necessary dependencies using pip: `pip install -r requirements.txt`

5. **Run the Tests**: Ensure that all tests pass with your local setup: `./scripts/test.sh`

6. **Generate Migrations**: Create your migrations automatically by executing `./scripts/revision.sh "my revision description"`

## Pull Request Process

Once you've made changes that you want to propose for merging into the main project, you can submit a pull request (PR). Here are the steps you should follow for submitting a PR:

1. **Fetch Upstream**: Update your local copy with the latest changes from the main repo: `git pull upstream main`

2. **Create a New Branch**: Create a new branch for your changes: `git checkout -b your-branch-name`

3. **Commit Your Changes**: After you've made your changes or improvements, commit them to your branch.

4. **Push to Your Fork**: Once you've committed all your changes, push the changes to your fork on GitHub: `git push origin your-branch-name`

5. **Submit a Pull Request**: Finally, navigate to your fork on GitHub and click the "New pull request" button. Fill out the PR form and submit it.

Our team will review your PR as soon as possible and provide constructive feedback. If your PR is approved, it will be merged into the main codebase.

Thank you once again for considering a contribution to CanaryPy. With your help, we can continue to improve CanaryPy, making it the go-to solution for safer and more controlled deployments.