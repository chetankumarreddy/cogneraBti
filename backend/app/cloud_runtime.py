import os
from pathlib import Path
from typing import Dict

SECRET_MOUNT_PATH = Path(os.getenv("BTI_SECRET_MOUNT_PATH", "/var/secrets/cognira-bti"))

def _read_secret_file(name: str) -> str:
    path = SECRET_MOUNT_PATH / name
    if path.exists():
        return path.read_text(encoding="utf-8").strip()
    return ""

def cloud_runtime_status() -> Dict[str, str | bool]:
    gcul_password_present = bool(os.getenv("BTI_GCUL_PASSWORD") or _read_secret_file("gcul-password"))
    eth_password_present = bool(os.getenv("BTI_ETHEREUM_RPC_PASSWORD") or _read_secret_file("ethereum-rpc-password"))
    admin_password_present = bool(os.getenv("BTI_ADMIN_PASSWORD") or _read_secret_file("admin-password"))
    return {
        "platform": os.getenv("BTI_PLATFORM_NAME", "Cognira BTI"),
        "project_id": os.getenv("BTI_GCP_PROJECT_ID", "not-set"),
        "region": os.getenv("BTI_GCP_REGION", "not-set"),
        "zone": os.getenv("BTI_GCP_ZONE", "not-set"),
        "ledger_mode": os.getenv("BTI_LEDGER_MODE", "mock_gcul"),
        "gcul_endpoint_configured": bool(os.getenv("BTI_GCUL_ENDPOINT")),
        "ethereum_rpc_configured": bool(os.getenv("BTI_ETHEREUM_RPC_URL")),
        "gcul_password_present": gcul_password_present,
        "ethereum_rpc_password_present": eth_password_present,
        "admin_password_present": admin_password_present,
        "secret_source": "mounted-secret-manager" if SECRET_MOUNT_PATH.exists() else "env-or-local"
    }
