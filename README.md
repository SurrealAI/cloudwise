# Cloudwise
[Installation](#installation)  
[Usage](#usage)  
[FAQs](#faqs)  

---

`cloudwise` is Surreal's cloud infrastructure provisioner based on Terraform. Surreal's [website](surreal.stanford.edu) and [github](https://github.com/SurrealAI/Surreal).

It prepares a kubernetes cluster using terraform. It generates `.tf.json` files that are also recognized by
[Symphony](https://github.com/SurrealAI/symphony). 

# Installation
* Cloud wise runs in python 3
* Do `git clone git@github.com:SurrealAI/cloudwise.git && cd cloudwise`
* Run `pip install -e .` in this directory.
* Install `terraform` following instructions [here](https://www.terraform.io/intro/getting-started/install.html)
* Install `kubectl` following instructions [here](https://kubernetes.io/docs/tasks/tools/install-kubectl/)

# Usage
* (Optional, Recommended) Create and work in a clean directory as running terraform would generate relevant files. 
```bash
> mkdir kurreal
> cd kurreal
```

* For Google Cloud, run 
```bash
> cloudwise-gke
```

* For AWS/Azure, stay tuned.
* The commandline helper will provide instructions and generate a `<cluster_name>.tf.json` file which terraform recognizes.
* `terraform init && terraform plan` describes changes to be made. 
* `terraform apply` makes the changes to your cloud project. 
* * If you want to remove everything, run `terraform destory`
* After cluster creation, obtain credentials for kubectl.
```bash
> gcoud container clusters get-credentials <cluster_name>
```
* If you have GPUs in your cluster, create the daemon set to install drivers, see [documentation](https://cloud.google.com/kubernetes-engine/docs/how-to/gpus#installing_drivers).
```bash
> kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/container-engine-accelerators/stable/nvidia-driver-installer/cos/daemonset-preloaded.yaml
```
* The generated `<cluster_name>.tf.json` is also recognized by [Symphony](https://github.com/SurrealAI/symphony)'s scheduling mechanism and `Surreal`. So you may want to link to it 

# FAQs:
* How do I create the authentication json for google cloud?  
You can see terraform guide [here](https://www.terraform.io/docs/providers/google/index.html) or search on google for reference. Essentially, go to [https://console.cloud.google.com/apis/credentials/serviceaccountkey](https://console.cloud.google.com/apis/credentials/serviceaccountkey) and select **Create new service account**. You would need to give the service account sufficient permissions to do things properly. **Project editor** would suffice but is also more than enough. You can then generate and download the key, (*json* format is fine). Put the path to the `.json` file into the commandline argument when prompted.

* I am seeing error: `Kubernetes Engine API has not been used in project...`  
If you see the following error during `terraform apply`, go to the Kubernetes Engine tab on your google cloud console.
```
Kubernetes Engine API has not been used in project ... before or it is disabled. Enable it by visiting https://console.developers.google.com/apis/api/container.googleapis.com/overview?project=... then retry.
```

* GPU nodes are not scaling up. Check if the driver installation daemon set is running (see [documentation](https://cloud.google.com/kubernetes-engine/docs/how-to/gpus#installing_drivers)).
