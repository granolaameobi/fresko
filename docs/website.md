# Fresko Website

## Overview

The Fresko website is a Flask web app deployed on a [Google Kubernetes Engine cluster](https://console.cloud.google.com/kubernetes/clusters/details/europe-west1/fresko-cluster-1/details?project=evident-zone-391812) and is accessible at [35.240.76.57](http://35.240.76.57/).

## Web App Structure

The Flask web app consists of a main Python script, [app.py](/app.py), that has app route decorated functions for every page on the website. All bar one of these functions simply renders a HTML template file, found under [templates/](/templates/). All bar one of these rendered templates are extensions of [base.html](/templates/base.html). This file works with [style.css](/static/css/style.css) to centralise the general style of the website, and allow the header and footer of the wesbite to be defined in one place. The [style.css](/static/css/style.css) file is found under the [static/](/static/) directory, where static files that are accessed by the web app are stored. These include image files for the website as well as [functions.py](/static/sql/functions.py) which a module that holds some functions that are used to query to SQL database in the app.
<br>
The exception to the rule of functions simply rendering templates is the `reservation()` function. This function handles two different API calls, `GET` and `POST`. The `GET` method simply renders the reservation form template. The `POST` method handles the form submission, runs functions which handle the assigning of available tables, writes the booking entry(ies) to the database (one row for each table ID assigned), and finally uses the email API to send a booking confirmation email and returning a similar confirmation on the website.
<br>
The exception to the rule of templates extending [base.html](/templates/base.html) is [email_confirmation.html](/templates/email_confirmation.html). This is because the email client is flaky in its CSS support and images are hidden by default. Therefore, this template is a standalone template that generates a minimalist email body.
<br>
The reservation part of the web app utilises several environmental variables. These are `FLASK_APP`, `MAIL_PASSWORD`, `DB_NAME`, `DB_USER` and `DB_PASSWORD`. The latter four are provided to the deployed application through Kubernetes secret mappings (see below).

## Kubernetes Deployment

### CI/CD Pipeline

The automating of the testing, building and deployment of the web app is handled by GitHub Actions. The workflow is defined in [.github/workflows/build-release.yaml](.github/workflows/build-release.yaml).
<br> 
The first stage of this pipeline runs on the opening of a Pull Request and tests if all the routes of the web app are returning `200` status codes as expected.
<br>
The next stage uses the [semantic-release](https://semantic-release.gitbook.io/semantic-release/) package to generate a new tag for the Docker Image and the repository (the config is found in [release.config.js](/release.config.js)). The [Dockerfile](/build/Dockerfile) is then used to build Docker Image of the application and it is tagged with the new tag number before being pushed to the [GitHub Container Registry](https://github.com/granolaameobi?tab=packages&repo_name=fresko). This new image is then rolled-out in the Kubernetes Deployment.

### Kubernetes Manifest File

The deployment is defined by the Kubernetes Manifest file in [deployment/web-app.yaml](/deployment/web-app.yaml). Declared inside this file is the configuration for a deployment, `my-website-deployment` and a service, `my-website-service`.

### Service and Pods

The deployment consists of two identical Kubernetes pods, this facilitates the website being highly-available, as if one pod crashes, the other is still accessible while it is being replaced. 
<br>
These pods do not have external IP addresses, and their transient nature makes them unsuitable for such. The service `my-website-service` provides an constant external IP address to the deployment, and acts a Load Balancer, balancing the network requests between the two pods.
<br>
As mentioned in [CI/CD Pipeline](#cicd-pipeline), the new Docker Images are rolled-out to the deployment. When this happens, one pod will be taken down while it is replaced with a pod with the new application, before the same happens to the other. This means there is no down-time on the website while the updates are being made.

### Cloud SQL Proxy Sidecar

When running the Flask app locally, `host` needs to be set to 35.205.66.81 and the local IP address needs to be added to [Authorised Networks](https://console.cloud.google.com/sql/instances/freskodb-23/connections/networking?project=evident-zone-391812). However, in the deployed application, the connection to the database is handled by a secondary application inside the pods. As well as the Flask web app running in the pods, the Google-managed Cloud SQL proxy application is also running. This "sidecar" application uses a mounted storage of Service Account (that has access to our Cloud SQL server) credentials to connect to the database and acts as a proxy such that the pod believes the application is running at 127.0.0.1 (localhost). Hence, 127.0.0.1 is the value we set as `host` in app.py in the deployed application.
<br>
A visual represntation of this process is shown here:
<img src='https://i.pinimg.com/originals/dd/37/21/dd3721c37b3a60521020288a2ecd63b9.png' alt='sidecar image'>

### Secrets

As mentioned, the Flask web app uses environment variables to handle the database connection and email client connection. These are mapped into the pods via two Kubernetes Secrets, `cloudsql-db-credentials` and `email-secrets`.

### Debugging the Deployment

#### Installing gcloud SDK and kubectl

In the event that the deployed website is not working through no obvious problem with the web app, two tools will need to be installed to interact with the GKE cluster. 
<br>
The first, gcloud CLI tool, can be installed following the steps [here](https://cloud.google.com/sdk/docs/install).
The next, kubectl (Kubernetes command-line interpreter), can be downloaded by following these [steps](https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/).

#### Connecting to Cluster

To set the context of kubectl to the GKE cluster, follow the steps [here](https://cloud.google.com/kubernetes-engine/docs/how-to/cluster-access-for-kubectl).<br>
Once this has been done, running `kubectl get deployments` should return "my-website-deployment".<br>
Running `kubectl get {manifest}` i.e `kubectl get pods` or `kubectl get secrets` or `kubectl get services` will return a quick overview of the state of the objects in the manifest you queried. <br>
Running `kubectl describe {object}` i.e `kubectl describe {pod name}` will give more detailed insight into the pod you want to look at.
A pod's logs can viewed for a pod with `kubectl logs {pod name}`. This will also allow you view what requests are being made to the website and the IP addresses that are making them.
A full list of kubectl commands can be found [here](https://kubernetes.io/docs/reference/kubectl/cheatsheet/).