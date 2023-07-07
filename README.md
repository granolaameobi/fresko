# Fresko 

![Fresko Logo](/docs/fresko.png)

## Overview
Central Repository for Fresko IT. Hosts code for Flask web app for Fresko website.

## Flask Web App
Main app file is found at [app.py](/app.py). Templates for different web pages are found under [templates/](/templates/). Currently the web app is simplistic with a few pages acting as placeholders. Reservations page is currently not backended by a database as this is a work in progress.

## CI/CD Pipeline
A GitHub Actions workflow is setup to carry out two jobs:
- Validating Pull Requests to `main` branch by running Pytests defined [here](/tests/test_boot.py)
- Releasing web app to production environment upon merge of valid Pull Requests

Currently, the tests assert that the web app can boot up and GET requests return `200` status code responses for each of the paths, as well as the POST request for the reservation form. <br>
The second job in the pipeline builds and publishes the web app Docker Image to GitHub Packages (in this repository). If tis build and push is a success, the new image is deployed to our Google Kubernetes Engine cluster using our Kubernetes manifests found in [/deployment/](/deployment/).

## Contributing
### Requirements
Before getting started, we recommended you have the following:
- Python 3.11 environment with packages in [/requirements.txt](/requirements.txt) installed
- working Docker Daemon

Once the repository is cloned to your local machine, assign the following environment variables:
- PYTHONPATH = base of this repository
- FLASK_APP = app.py

Once this is done, the app can be spun up locally with `flask run` and can then be viewed at [`localhost:5000`](http://localhost:5000).
### Branch Protection Rules
There are branch protection rules configured in this repository such that commits cannot be pushed directly to `main` branch. Therefore, to push code to `main`, open a new branch with `git checkout -b <branch name>`, commit to the changes, publish the new branch to the remote repository, and open a Pull Request.<br>
 Note: Pull Requests can only be merged once the checks have passed (once the Pytests have passed in the GitHub Actions agent).
