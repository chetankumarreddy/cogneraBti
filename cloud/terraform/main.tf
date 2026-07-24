locals {
  labels = { app = "cognira-bti", environment = var.environment }
  secret_names = ["cognira-bti-gcul-password", "cognira-bti-ethereum-rpc-password", "cognira-bti-admin-password"]
}

resource "google_project_service" "apis" {
  for_each = toset([
    "container.googleapis.com",
    "artifactregistry.googleapis.com",
    "compute.googleapis.com",
    "secretmanager.googleapis.com",
    "cloudkms.googleapis.com",
    "logging.googleapis.com",
    "monitoring.googleapis.com",
    "iam.googleapis.com"
  ])
  project = var.project_id
  service = each.key
  disable_on_destroy = false
}

resource "google_artifact_registry_repository" "repo" {
  depends_on = [google_project_service.apis]
  location = var.region
  repository_id = var.artifact_repo
  description = "Cognira BTI containers"
  format = "DOCKER"
  labels = local.labels
}

resource "google_compute_network" "vpc" {
  name = var.network_name
  auto_create_subnetworks = false
  depends_on = [google_project_service.apis]
}

resource "google_compute_subnetwork" "subnet" {
  name = "${var.network_name}-subnet"
  ip_cidr_range = var.subnet_cidr
  region = var.region
  network = google_compute_network.vpc.id
  secondary_ip_range { range_name = "pods" ip_cidr_range = var.pods_cidr }
  secondary_ip_range { range_name = "services" ip_cidr_range = var.services_cidr }
}

resource "google_service_account" "gke_nodes" {
  account_id = "cognira-bti-gke-nodes"
  display_name = "Cognira BTI GKE node service account"
}

resource "google_service_account" "workload" {
  account_id = "cognira-bti-workload"
  display_name = "Cognira BTI workload identity service account"
}

resource "google_project_iam_member" "node_artifact_reader" {
  project = var.project_id
  role = "roles/artifactregistry.reader"
  member = "serviceAccount:${google_service_account.gke_nodes.email}"
}

resource "google_project_iam_member" "workload_secret_accessor" {
  project = var.project_id
  role = "roles/secretmanager.secretAccessor"
  member = "serviceAccount:${google_service_account.workload.email}"
}

resource "google_project_iam_member" "workload_logging" {
  project = var.project_id
  role = "roles/logging.logWriter"
  member = "serviceAccount:${google_service_account.workload.email}"
}

resource "google_container_cluster" "gke" {
  provider = google-beta
  name = var.cluster_name
  location = var.region
  deletion_protection = false
  remove_default_node_pool = true
  initial_node_count = 1
  network = google_compute_network.vpc.id
  subnetwork = google_compute_subnetwork.subnet.id
  ip_allocation_policy {
    cluster_secondary_range_name = "pods"
    services_secondary_range_name = "services"
  }
  workload_identity_config { workload_pool = "${var.project_id}.svc.id.goog" }
  secret_manager_config { enabled = true }
  release_channel { channel = "REGULAR" }
  addons_config { http_load_balancing { disabled = false } }
  depends_on = [google_project_service.apis]
}

resource "google_container_node_pool" "primary" {
  name = "cognira-bti-primary"
  location = var.region
  cluster = google_container_cluster.gke.name
  node_count = var.gke_min_nodes
  autoscaling { min_node_count = var.gke_min_nodes max_node_count = var.gke_max_nodes }
  node_config {
    service_account = google_service_account.gke_nodes.email
    machine_type = var.gke_node_machine_type
    oauth_scopes = ["https://www.googleapis.com/auth/cloud-platform"]
    labels = local.labels
  }
}

resource "google_secret_manager_secret" "gcul_password" {
  secret_id = "cognira-bti-gcul-password"
  replication { auto {} }
  labels = local.labels
}
resource "google_secret_manager_secret_version" "gcul_password" {
  count = var.gcul_secret_password == null ? 0 : 1
  secret = google_secret_manager_secret.gcul_password.id
  secret_data = var.gcul_secret_password
}
resource "google_secret_manager_secret" "eth_rpc_password" {
  secret_id = "cognira-bti-ethereum-rpc-password"
  replication { auto {} }
  labels = local.labels
}
resource "google_secret_manager_secret_version" "eth_rpc_password" {
  count = var.ethereum_rpc_password == null ? 0 : 1
  secret = google_secret_manager_secret.eth_rpc_password.id
  secret_data = var.ethereum_rpc_password
}
resource "google_secret_manager_secret" "admin_password" {
  secret_id = "cognira-bti-admin-password"
  replication { auto {} }
  labels = local.labels
}
resource "google_secret_manager_secret_version" "admin_password" {
  count = var.app_admin_password == null ? 0 : 1
  secret = google_secret_manager_secret.admin_password.id
  secret_data = var.app_admin_password
}

resource "google_compute_firewall" "eth_rpc_internal" {
  name = "cognira-bti-eth-rpc-internal"
  network = google_compute_network.vpc.name
  allow { protocol = "tcp" ports = ["8545", "8546", "30303"] }
  source_ranges = [var.subnet_cidr, var.pods_cidr]
  target_tags = ["cognira-bti-eth-rpc"]
}

resource "google_compute_instance" "ethereum_rpc" {
  name = "cognira-bti-eth-rpc"
  zone = var.zone
  machine_type = var.ethereum_rpc_machine_type
  tags = ["cognira-bti-eth-rpc"]
  boot_disk {
    initialize_params { image = "ubuntu-os-cloud/ubuntu-2204-lts" size = var.ethereum_rpc_disk_gb type = "pd-balanced" }
  }
  network_interface { subnetwork = google_compute_subnetwork.subnet.id }
  metadata_startup_script = file("${path.module}/startup-ethereum-rpc.sh")
  labels = local.labels
  depends_on = [google_project_service.apis]
}
