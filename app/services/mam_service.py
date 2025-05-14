class MockMAMClient:
    def push_metadata(self, asset_id: str, metadata: dict):
        print(f"[MAM] Updated asset {asset_id} with metadata: {metadata}")
        # Could simulate an HTTP POST to real MAM API here
