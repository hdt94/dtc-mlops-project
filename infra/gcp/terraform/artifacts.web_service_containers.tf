resource "google_artifact_registry_repository" "web_containers" {
  depends_on = [
    google_project_service.artifacts
  ]

  description   = "Docker repository for web service container images"
  format        = "DOCKER"
  location      = var.region
  repository_id = "web-containers"
}

output "web_containers" {
  value = {
    registry_host = "${var.region}-docker.pkg.dev"
    registry_url  = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.web_containers.repository_id}"
  }
}
