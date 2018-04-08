// Configure the Google Cloud provider
provider "google" {
//  credentials = "${file("account.json")}"
  project     = "humanlearn2-165719"
  // region      = "us-central1"
  zone = "us-west1-b"
}

# https://registry.terraform.io/modules/hashicorp/consul/google/0.0.1?tab=inputs

// Create a new instance
resource "google_compute_instance" "default" {
  name         = "aterra"
  machine_type = "n1-standard-1"
  zone         = "us-west1-b"

  tags = ["tagfoo", "tagbar"]
  allow_stopping_for_update = true

  provisioner "local-exec" {
    command = "echo hello terra ${self.instance_id} > shit.txt"
//    working_dir = "/home/"
//    interpreter = ["/bin/bash"]
  }

  boot_disk {
    initialize_params {
      # https://cloud.google.com/compute/docs/images
      image = "ubuntu-os-cloud/ubuntu-1604-lts"
      size = 23
    }
  }

  // Local SSD disk
  scratch_disk {
  }

  network_interface {
    network = "default"

    access_config {
      // Ephemeral IP
    }
  }

  metadata {
    metafoo = "mymetafoo"
  }

  metadata_startup_script = "echo hi > /test.txt"

  service_account {
    scopes = ["userinfo-email", "compute-ro", "storage-ro"]
  }
}

output "instid" {
  value = "${google_compute_instance.default.instance_id}"
}
