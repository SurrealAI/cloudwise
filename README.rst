Cloudwise
=========

| `Installation <#installation>`__
| `Usage <#usage>`__
| `FAQs <#faqs>`__

--------------

``cloudwise`` is Surreal’s cloud infrastructure provisioner based on
Terraform. Surreal’s `website <surreal.stanford.edu>`__ and
`github <https://github.com/SurrealAI/Surreal>`__.

It prepares a kubernetes cluster using terraform. It generates
``.tf.json`` files that are also recognized by
`Symphony <https://github.com/SurrealAI/symphony>`__.

Installation
============

-  Cloud wise runs in python 3
-  Do
   ``git clone git@github.com:SurrealAI/cloudwise.git && cd cloudwise``
-  Run ``pip install -e .`` in this directory.
-  Install ``terraform`` following instructions
   `here <https://www.terraform.io/intro/getting-started/install.html>`__
-  Install ``kubectl`` following instructions
   `here <https://kubernetes.io/docs/tasks/tools/install-kubectl/>`__

Usage
=====

-  (Optional, Recommended) Create and work in a clean directory as
   running terraform would generate relevant files.

.. code:: bash

   > mkdir surreal
   > cd surreal

Google Cloud
------------

-  You first need to setup credentials for ``terraform`` to access
   google cloud. See guide
   `here <https://www.terraform.io/docs/providers/google/provider_reference.html>`__.
   Choose one of the two methods:

   -  Run the following command

   .. code:: bash

      gcloud auth application-default login

   or

   -  Go to the api key management page
      https://console.cloud.google.com/apis/credentials/serviceaccountkey
      and select **Create new service account**. You would need to give
      the service account sufficient permissions to do things properly.
      **Project editor** would suffice but is also more than enough. You
      can then generate and download the key, (*json* format is fine).
      Put the path to the ``.json`` file into the commandline argument
      when prompted.

-  Follow the instructions in the commandline tool.

.. code:: bash

   > cloudwise-gke

It will provide instructions and generate a ``<cluster_name>.tf.json``
file which terraform recognizes. If you have generated a ``.json``
credential file, you should provide it when prompted. \*
``terraform init && terraform plan`` describes changes to be made. \*
``terraform apply`` makes the changes to your cloud project. \* After
cluster creation, obtain credentials for kubectl.

.. code:: bash

   > gcloud container clusters get-credentials <cluster_name>

-  If you have GPUs in your cluster, create the daemon set to install
   drivers, see
   `documentation <https://cloud.google.com/kubernetes-engine/docs/how-to/gpus#installing_drivers>`__.

.. code:: bash

   > kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/container-engine-accelerators/stable/nvidia-driver-installer/cos/daemonset-preloaded.yaml

-  The generated ``<cluster_name>.tf.json`` is also recognized by
   `Symphony <https://github.com/SurrealAI/symphony>`__\ ’s scheduling
   mechanism and ``Surreal``. So you may want to link to it
-  If you want to remove everything, run ``terraform destroy``

AWS
---

Stay tuned

Azure
-----

Stay tuned

FAQs:
=====

-  Terraform install fails.

   -  If you are seeing error:
      ``... API has not been used in project...``: during
      ``terraform apply``, go to the Kubernetes Engine tab and/or
      Compute Engine tab on your google cloud console to enable their
      APIs.

-  GPU nodes are not scaling up.

   -  Check if the driver installation daemon set is running (see
      `documentation <https://cloud.google.com/kubernetes-engine/docs/how-to/gpus#installing_drivers>`__).
