resource "google_storage_bucket" "ml_models" {
  name     = "ml-models-${var.project_id}"
  location = var.region

  force_destroy               = true
  storage_class               = "STANDARD"
  uniform_bucket_level_access = true

  versioning {
    enabled = false
  }
}

output "ml_models_bucket" {
  value = {
    id        = google_storage_bucket.ml_models.id
    self_link = google_storage_bucket.ml_models.self_link
    url       = google_storage_bucket.ml_models.url
  }
}
