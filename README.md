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

Confirm image in the `demo` project image stream with `oc get is`.

* Update `helm/values.yaml` with username and token, obtained using `oc whoami -t`. Ensure namespace is also set to `demo`. Commit and push changes to GitHub.

* Ensure or install operators "Red Hat OpenShift Pipelines" and "Red Hat OpenShift GitOps"

* Deploy ArgoCD in the `demo` project via the web console, "Installed Operators" -> Redh Hat OpenShift GitOps" -> "ArgoCD" -> "Create ArgoCD". Once deployed, visit the topology of the `demo` project to view the argocd deployed components and find the URL for the argocd-server. 

* Log into ArgoCD, find the `admin` password under "Workloads" -> "Secrets" -> `argocd-cluster`. 

* In ArgoCD create a new app using:

Project: defualt
Repo: https://github.com/rwalker-redhat/fastapi-quickstart-project.git
Target: HEAD
Path: helm
Dest: in-cluster
Namespace: demo

**The application should now be deployed and working using the helm chart via ArgoCD.**

* Create a pvc called `shared-workspace` 

* Add first two-step pipeline `oc create -f ocp/demo/pipeline-demo-1.yaml`. Run the pipeline via the web console, selecting the pvc for the workspace. Validate the new tag number once completed with `oc get is`.

* Pytest should be availble via the Pipeline Builder, but if not add the task from https://hub.tekton.dev/tekton/task/pytest first, then insert the task prior to the build task.

* Repeat for adding the `yq` task, https://hub.tekton.dev/tekton/task/yq - and update pipeline adding `yq` after the build task.`

`helm/values.yaml`
`.tag = $(params.IMAGE_TAG)`

* Create an SSH key pair `ssh-keygen -f pipeline`, add the public key to GitHub and the private key to OpenShift using `oc create secret generic pipeline-ssh-key --from-file pipeline --from-file=known_hosts=known_hosts`. The `known_host` file just needs the `github.com...` host line in it. 

* Add a `git-cli` task, a Clustertask will be availble for this one, so this step can be done directly in the pipeline yaml, including the extra workspace `ssh-creds` for example:

```
    - name: git-cli
      params:
        - name: BASE_IMAGE
          value: >-
            docker.io/alpine/git:v2.26.2@sha256:23618034b0be9205d9cc0846eb711b12ba4c9b468efdd8a59aac1d7b1a23363f
        - name: GIT_SCRIPT
          value: >
            git add helm/values.yaml

            git commit -m "updated tag via pipeline" --allow-empty

            git remote set-url origin
            git@github.com:rwalker-redhat/fastapi-quickstart-project.git


            export GIT_SSH_COMMAND="ssh -i /root/.ssh/pipeline -o
            'IdentitiesOnly yes'"


            git push origin HEAD:$(params.GIT_REVISION)
        - name: USER_HOME
          value: /root
        - name: VERBOSE
          value: 'true'
        - name: GIT_USER_NAME
          value: rwalker-redhat
        - name: GIT_USER_EMAIL
          value: rwalker@redhat.com
      runAfter:
        - yq
      taskRef:
        kind: ClusterTask
        name: git-cli
      workspaces:
        - name: source
          workspace: workspace
        - name: ssh-directory
          workspace: ssh-creds
  workspaces:
    - name: workspace
    - name: ssh-creds
```

* OPTIONAL - argocd will poll every 3 mins regardless. Repeat for adding the `argocd` task, https://hub.tekton.dev/tekton/task/argocd-task-sync-and-wait - and update the pipeline adding `argocd` after the `gitcli` task.





# Event Listener



To list `oc get triggers.triggers.tekton.dev`.

To describe `oc describe triggers.triggers.tekton.dev fastapi-trigger`.


To list event listeners `oc get el`.

Once the Envent Lister is added, create a route by exposing the service with `oc expose service/el-fastapi-ev`

Under the repos settings in GitHub, select Webhooks, enter the Payload URL with content type "application/json" and "Just the `push` event".