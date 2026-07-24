output "artifact_registry" { value = "${var.region}-docker.pkg.dev/${var.project_id}/${var.artifact_repo}" }
output "gke_cluster" { value = google_container_cluster.gke.name }
output "gke_region" { value = var.region }
output "ethereum_rpc_internal_url" { value = "http://${google_compute_instance.ethereum_rpc.network_interface[0].network_ip}:8545" }
output "workload_service_account" { value = google_service_account.workload.email }
output "kubernetes_workload_identity_member" { value = "serviceAccount:${var.project_id}.svc.id.goog[cognira-bti/cognira-bti-ksa]" }
