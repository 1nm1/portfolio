

provider "google" {
  credentials = file(var.credentials_file)

  project = var.project
  region  = var.region
}

resource "google_compute_instance" "default" {
  name         = "compute-dev-api"
  machine_type = "f1-micro"
  zone         = var.zone

  tags = ["project", "prod-api"]

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
    # Google recommends custom service accounts that have cloud-platform scope and permissions granted via IAM Roles.
    email  = var.service_account_email
    scopes = ["cloud-platform"]
  }
}