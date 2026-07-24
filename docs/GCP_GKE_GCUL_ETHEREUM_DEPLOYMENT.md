# Cognira BTI Hackathon Deployment on Google Cloud GKE, GCUL and Ethereum RPC

This package is aligned for a Google Cloud deployment using:

- Google Kubernetes Engine for API and React workloads
- Artifact Registry for container images
- Secret Manager for passwords/tokens
- Workload Identity Federation for GKE workloads
- GCUL endpoint configuration through ConfigMap and Secret Manager
- Ethereum RPC node on Compute Engine inside the same VPC

## Important password handling rule

Do not place passwords in Git, YAML, Dockerfiles, Terraform files or README text. Use:

```bash
./cloud/scripts/create_or_update_secrets.sh
```

The script prompts for:

- GCUL password/token
- Ethereum RPC password/token, if required
- Cognira BTI admin password

and writes them to Google Secret Manager.

## Location details

Set location in:

```bash
cloud/scripts/set_env.sh
```

or export before running:

```bash
export PROJECT_ID="your-gcp-project-id"
export REGION="europe-west2"
export ZONE="europe-west2-a"
export CLUSTER_NAME="cognira-bti-gke"
export GCUL_ENDPOINT="https://gcul.example.internal/rpc"
export GCUL_CHAIN_ID="gcul-hackathon"
```

## Full deployment

```bash
./cloud/scripts/full_gke_deploy.sh
```

## Step-by-step deployment

```bash
./cloud/scripts/bootstrap_gcp.sh
./cloud/scripts/create_or_update_secrets.sh
./cloud/scripts/build_and_push.sh
./cloud/scripts/deploy_gke.sh
```

## Validate runtime

```bash
kubectl -n cognira-bti get pods
kubectl -n cognira-bti get svc cognira-bti-web
kubectl -n cognira-bti port-forward svc/cognira-bti-api 8000:8000
curl http://localhost:8000/cloud/runtime
```

## Terraform input examples

```bash
export TF_VAR_project_id="your-gcp-project-id"
export TF_VAR_region="europe-west2"
export TF_VAR_zone="europe-west2-a"
export TF_VAR_gcul_secret_password="do-not-commit"
export TF_VAR_ethereum_rpc_password="do-not-commit"
export TF_VAR_app_admin_password="do-not-commit"
```

Prefer the interactive Secret Manager script for passwords during hackathon execution.
