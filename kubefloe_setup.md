run powershell as admin 


to install minikube

New-Item -Path 'c:\' -Name 'minikube' -ItemType Directory -Force
$ProgressPreference = 'SilentlyContinue'; Invoke-WebRequest -OutFile 'c:\minikube\minikube.exe' -Uri 'https://github.com/kubernetes/minikube/releases/latest/download/minikube-windows-amd64.exe' -UseBasicParsing



Add binary  system path

$oldPath = [Environment]::GetEnvironmentVariable('Path', [EnvironmentVariableTarget]::Machine)
if ($oldPath.Split(';') -inotcontains 'C:\minikube'){
  [Environment]::SetEnvironmentVariable('Path', $('{0};C:\minikube' -f $oldPath), [EnvironmentVariableTarget]::Machine)
}


Start your cluster
minikube start




setup Kubectl



Install kubectl binary on Windows (via direct download or curl)
You have two options for installing kubectl on your Windows device

Direct download:

Download the latest 1.33 patch release binary directly for your specific architecture by visiting the Kubernetes release page. Be sure to select the correct binary for your architecture (e.g., amd64, arm64, etc.).

Using curl:

If you have curl installed, use this command:

curl.exe -LO "https://dl.k8s.io/release/v1.33.0/bin/windows/amd64/kubectl.exe"
Note:
To find out the latest stable version (for example, for scripting), take a look at https://dl.k8s.io/release/stable.txt.
Validate the binary (optional)

Download the kubectl checksum file:

curl.exe -LO "https://dl.k8s.io/v1.33.0/bin/windows/amd64/kubectl.exe.sha256"
Validate the kubectl binary against the checksum file:

Using Command Prompt to manually compare CertUtil's output to the checksum file downloaded:

CertUtil -hashfile kubectl.exe SHA256
type kubectl.exe.sha256
Using PowerShell to automate the verification using the -eq operator to get a True or False result:

 $(Get-FileHash -Algorithm SHA256 .\kubectl.exe).Hash -eq $(Get-Content .\kubectl.exe.sha256)
Append or prepend the kubectl binary folder to your PATH environment variable.

Test to ensure the version of kubectl is the same as downloaded:

kubectl version --client
Or use this for detailed view of version:

kubectl version --client --output=yaml




to setup Kubeflow 


since we are using minikube nd kubectl we dont need to follow first 2 step from official guideline which shows to start kubenetes from docker desktop in-built one.

To deploy the Kubeflow Pipelines, run the following commands:

# use set for windwos and export for Linux based system for below line
set PIPELINE_VERSION=2.4.0
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION"
kubectl wait --for condition=established --timeout=60s crd/applications.app.k8s.io
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/env/platform-agnostic?ref=$PIPELINE_VERSION"
The Kubeflow Pipelines deployment may take several minutes to complete.

Verify that the Kubeflow Pipelines UI is accessible by port-forwarding:

check all pods are running though - 'kubectl get pod -A'

kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8080:80

Then, open the Kubeflow Pipelines UI at http://localhost:8080/ or - if you are using kind or K3s within a virtual machine - http://{YOUR_VM_IP_ADDRESS}:8080/

Note that K3ai will automatically print the URL for the web UI at the end of the installation process.




# push your project docker imager to dockerhub

docker build -t my-project .
docker run my-project

docker login
#login to your dockerimage account

docker tag my-project username_dockerhub/my-project:latest
docker push username_dockerhub/my-project:latest




after this write the kubeflow_pipeline/mlops_pipeline.py 
since we are using dagshub
you would need
kubectl create secret generic dagshub-secret \
  --from-literal=DAGSHUB_USERNAME=avnishs17 \
  --from-literal=DAGSHUB_TOKEN=bdba201ba0b2d84838403a0dc4525cd0e18a54e5 \
  -n kubeflow


to run 
kubectl create secret generic dagshub-secret --from-literal=DAGSHUB_USERNAME=avnishs17 --from-literal=DAGSHUB_TOKEN=bdba201ba0b2d84838403a0dc4525cd0e18a54e5

aftet this kubeflow_pipeline/mlops_pipeline.py   from this we will bet the yaml files that we will use 

then go to localhost:8080   # make sure 'kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8080:80' this command is still running and listening on port 8080

select upload pipeline -> create new pipeline -> give the name -> select upload file and upload the 'mlops_pipeline.yaml' file created by running kubeflow_pipeline/mlops_pipeline.py
-> click create
after this -> goto create run -> click experiments -> give experiment name -> then click next -> choose the pipeline we created earlier -> use deafult run name or give new name -> choose the experiment to associate the run with -> select run type as one-off and click start

wait for some time it should finish and 
Note: kubectl apply -k accepts local paths and paths that are formatted as hashicorp/go-getter URLs. While the paths in the preceding commands look like URLs, they are not valid URLs.

Uninstalling Kubeflow Pipelines
Below are the steps to remove Kubeflow Pipelines on kind, K3s, or K3ai:

To uninstall Kubeflow Pipelines using your manifest file, run the following command, replacing {YOUR_MANIFEST_FILE} with the name of your manifest file:

kubectl delete -k {YOUR_MANIFEST_FILE}`
To uninstall Kubeflow Pipelines using manifests from Kubeflow Pipelines’s GitHub repository, run these commands:

export PIPELINE_VERSION=2.4.0
kubectl delete -k "github.com/kubeflow/pipelines/manifests/kustomize/env/platform-agnostic?ref=$PIPELINE_VERSION"
kubectl delete -k "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION"
To uninstall Kubeflow Pipelines using manifests from your local repository or file system, run the following commands:

kubectl delete -k manifests/kustomize/env/platform-agnostic
kubectl delete -k manifests/kustomize/cluster-scoped-resources