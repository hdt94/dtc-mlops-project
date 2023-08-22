resource "google_project_service" "artifacts" {
  disable_on_destroy = false
  project            = data.google_project.project.project_id
  service            = "artifactregistry.googleapis.com"
}

resource "google_project_service" "build" {
  disable_on_destroy = false
  project            = data.google_project.project.project_id
  service            = "cloudbuild.googleapis.com"
}

resource "google_project_service" "run" {
  disable_on_destroy = false
  project            = var.project_id
  service            = "run.googleapis.com"
}
