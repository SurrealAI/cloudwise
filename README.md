# Cloudwise

`cloudwise` is our cloud infrastructure provisioner based on Terraform. 

It prepares the playground for the [`symphony` orchestration engine](https://github.com/SurrealAI/symphony). 

[Google doc](https://goo.gl/hbfbrC)

# Installation
* Do `git clone git@github.com:SurrealAI/cloudwise.git && cd cloudwise`
* Run `pip install -e .` in this directory.
* Install terraform following instructions [here](https://www.terraform.io/intro/getting-started/install.html)

# Usage
* (Optional, Recommended) Create and work in a clean directory as running terraform would generate relevant files. 
* For Google Cloud, run `cloudwise-gke`. 
* For AWS/Azure, stay tuned.
* The commandline helper will provide instructions and generate a `.tf.json` file which terraform recognizes.
* As the commandline tools would also tell you, `terraform init && terraform plan` describes changes to be made. `terraform apply` makes the changes to your cloud project. 

* If you want to remove everything, run `terraform destory`

# FAQs:
* How do I create the authentication json for google cloud?
You can see terraform guide [here](https://www.terraform.io/docs/providers/google/index.html) or search on google for reference. Essentially, go to [https://console.cloud.google.com/apis/credentials/serviceaccountkey](https://console.cloud.google.com/apis/credentials/serviceaccountkey) and select **Create new service account**. You would need to give the service account sufficient permissions to do things properly. **Project editor** would suffice but is also more than enough. You can then generate and download the key, (*json* format is fine). Put the path to the `.json` file into the commandline argument when prompted.

* I am seeing error: `Kubernetes Engine API has not been used in project...`
If you see the following error during `terraform apply`, go to the Kubernetes Engine tab on your google cloud console.
```
Kubernetes Engine API has not been used in project ... before or it is disabled. Enable it by visiting https://console.developers.google.com/apis/api/container.googleapis.com/overview?project=... then retry.
```

