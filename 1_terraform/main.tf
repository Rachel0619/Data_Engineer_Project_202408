terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.1.0"
    }
  }
}

provider "google" {
  project = "firm-capsule-435019-c6"
  region  = "us-central1"
}

resource "google_storage_bucket" "demo-bucket" {
  name          = "firm-capsule-435019-c6-terra-bucket"
  location      = "US"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}