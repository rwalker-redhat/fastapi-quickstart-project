# fastapi-quickstart-project

## Runnign code on RHEL8

Clone this repository:

```shell
git clone https://github.com/rwalker-redhat/fastapi-quickstart-project.git
```

Change into the project directory:

```shell
cd fastapi-quickstart-project
```

Install Python 3.x

```shell
dnf module enable python39
```

```shell
dnf install python3.9
```

Create a Python Virtual Environment:

```shell
python3.9 -m venv venv
````

Activate and install requirements:

```shell
. venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt 
```

Run application:

```shell
python main.py
```

## OpenShift 

* Log into OpenShift cluster via CLI

* Create new project `oc new-project demo`

* Ensure or expose a route for the OpenShift image registry.

`oc patch configs.imageregistry.operator.openshift.io/cluster --patch '{"spec":{"defaultRoute":true}}' --type=merge -n openshift-image-registry`

* Log into registory using Podman.

`oc get route -n openshift-image-registry`

`podman login -u developer -p $(oc whoami -t) --tls-verify=false <ROUTE>`

* Build, tag and push the application image.

`podman build -t local/fastapi-quickstart-img:1.0 .`

`podman tag localhost/local/fastapi-quickstart-img:1.0 default-route-openshift-image-registry.apps.<CLUSTER>/demo/fastapi-quickstart-img:1.0`

`podman push default-route-openshift-image-registry.apps.<CLUSTER>/demo/fastapi-quickstart-img:1.0`

* Update `helm/values.yaml` with username and token, obtained using `oc whoami -t`. Ensure namespace is also set to `demo`. Commit and push changes to GitHub.

* Ensure or install operators "Red Hat OpenShift Pipelines" and "Red Hat OpenShift GitOps"

* Deploy ArgoCD in the `demo` project via the web console, "Installed Operators" -> Redh Hat OpenShift GitOps" -> "ArgoCD" -> "Create ArgoCD". Once deployed, visit the topology of the `demo` project to view the argocd deployed components and find the URL for the argocd-server. 

* Log into ArgoCD, find the `admin` password under "Workloads" -> "Secrets" -> `argocd-cluster`. 