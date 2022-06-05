

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

  network_interface {
    network = "default"
  }

  metadata = {
    project = "dev-api"
  }

  service_account {
    email  = var.service_account_email
    scopes = ["cloud-platform"]
  }
}