

provider "google" {
  credentials = file("key.json")

  project = "<project>"
  region  = "us-west2"
}

resource "google_compute_instance" "default" {
  name         = "compute-dev-api"
  machine_type = "f1-micro"
  zone         = "us-west2-a"

  tags = ["project", "dev-api"]

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-9"
    }
  }

  // Local SSD disk
#   scratch_disk {
#     interface = "NVME"
#   }

  network_interface {
    network = "default"

    access_config {
      // Ephemeral public IP
    }
  }

  metadata = {
    project = "dev-api"
  }

  //metadata_startup_script = "echo hi > /test.txt"

  service_account {
    
    email  = "<service-account@email.address.com>"
    scopes = ["cloud-platform"]
  }
}