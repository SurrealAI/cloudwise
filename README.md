# Cloudwise

`cloudwise` is our cloud infrastructure provisioner based on Terraform. 

It prepares the playground for the [`symphony` orchestration engine](https://github.com/SurrealAI/symphony). 

[Google doc](https://goo.gl/hbfbrC)




FAQs:

If you see the following error during `terraform apply`, go to the Kubernetes Engine tab on your google cloud console.
```
Kubernetes Engine API has not been used in project ... before or it is disabled. Enable it by visiting https://console.developers.google.com/apis/api/container.googleapis.com/overview?project=... then retry.
```
