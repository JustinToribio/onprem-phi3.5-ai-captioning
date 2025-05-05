from pathlib import Path
from huggingface_hub import snapshot_download
import os

def download_phi3_onnx_int4():
    """
    Downloads the smallest available Phi-3 Vision ONNX CUDA model (INT4 precision)
    from Hugging Face and saves it locally.
    """
    # Define the destination directory for the downloaded model
    destination = Path(__file__).resolve().parents[2]/"onnx_models"
    destination.mkdir(parents=True, exist_ok=True)

    # Define the model repository and the allowed patterns for the download
    model_repo = "microsoft/Phi-3-vision-128k-instruct-onnx-cuda"
    allow_patterns = ["cuda-int4-rtn-block-32/*"]

    # Download the model from the Hugging Face Hub
    print(f"Downloading INT4 ONNX CUDA model from '{model_repo}'...")
    snapshot_download(
        repo_id=model_repo,
        allow_patterns=allow_patterns,
        local_dir=str(destination)
    )
    print(f"Model downloaded to: {os.path.abspath(destination)}")

if __name__ == "__main__":
    download_phi3_onnx_int4()
