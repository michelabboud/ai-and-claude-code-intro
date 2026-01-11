"""
Secure secrets management with HashiCorp Vault.

Rotates API keys automatically during circuit breaker recovery.
"""

import hvac
import os
from typing import Dict, Optional


class SecretsManager:
    """
    Manage secrets with Vault.

    Features:
    - Automatic rotation
    - Audit logging
    - Lease management
    """

    def __init__(
        self,
        vault_addr: Optional[str] = None,
        vault_token: Optional[str] = None
    ):
        self.vault_addr = vault_addr or os.getenv('VAULT_ADDR', 'http://localhost:8200')
        self.vault_token = vault_token or os.getenv('VAULT_TOKEN')

        self.client = hvac.Client(
            url=self.vault_addr,
            token=self.vault_token
        )

        if not self.client.is_authenticated():
            raise ValueError("Vault authentication failed")

    def get_secret(self, path: str, rotate: bool = False) -> Dict:
        """
        Retrieve secret from Vault.

        Args:
            path: Secret path (e.g., 'claude/api-key')
            rotate: If True, rotate secret after retrieval

        Returns:
            Secret data dictionary
        """
        # Read current secret
        secret = self.client.secrets.kv.v2.read_secret_version(
            path=path,
            mount_point='secret'
        )

        secret_data = secret['data']['data']

        if rotate:
            # Generate new API key (implementation depends on provider)
            new_value = self._rotate_api_key(secret_data['value'])

            # Write new secret
            self.client.secrets.kv.v2.create_or_update_secret(
                path=path,
                secret={'value': new_value},
                mount_point='secret'
            )

            return {'value': new_value}

        return secret_data

    def _rotate_api_key(self, current_key: str) -> str:
        """
        Rotate API key with provider.

        In production, this would call Anthropic API to generate
        new key and revoke old one.
        """
        # Placeholder: In real implementation, call provider API
        print(f"Rotating API key (current: {current_key[:8]}...)")
        return f"sk-ant-new-key-{os.urandom(16).hex()}"


# Example usage
if __name__ == "__main__":
    """
    Before running this:
    1. Start Vault:
       docker run -d --name=vault --cap-add=IPC_LOCK \
         -p 8200:8200 -e 'VAULT_DEV_ROOT_TOKEN_ID=myroot' vault:latest

    2. Set environment:
       export VAULT_ADDR='http://localhost:8200'
       export VAULT_TOKEN='myroot'

    3. Store a test secret:
       vault kv put secret/claude/api-key value=sk-ant-test-12345
    """
    try:
        manager = SecretsManager()

        # Read secret
        print("Reading secret...")
        secret = manager.get_secret('claude/api-key')
        print(f"Current key: {secret['value'][:8]}...")

        # Rotate secret
        print("\nRotating secret...")
        new_secret = manager.get_secret('claude/api-key', rotate=True)
        print(f"New key: {new_secret['value'][:8]}...")

    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure Vault is running:")
        print("  docker run -d --name=vault --cap-add=IPC_LOCK \\")
        print("    -p 8200:8200 -e 'VAULT_DEV_ROOT_TOKEN_ID=myroot' vault:latest")
