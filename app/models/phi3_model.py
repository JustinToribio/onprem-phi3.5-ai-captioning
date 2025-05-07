from transformers import AutoModelForCausalLM, AutoProcessor
from app.core.config import model_id

# Offical docs on the inference code below: https://huggingface.co/microsoft/Phi-3.5-vision-instruct

class Phi3Model:
    # Class-level (shared) variables to store model and processor
    # When the model and processor are loaded for the first time, they'll be stored here
    _model = None
    _processor = None

    @classmethod
    def load(cls):
        # If not already loaded, load the model and processor once
        # Model and artifacts are downloaded to ~/.cache/huggingface
        if cls._model is None or cls._processor is None:
            cls._model = AutoModelForCausalLM.from_pretrained(
                model_id,
                device_map="cuda",               # Load model onto GPU
                trust_remote_code=True,           # Enable custom model class
                torch_dtype="auto",              # Use optimal precision (e.g. bf16)
                _attn_implementation="eager"      # Fallback for non-flash attention environments
            )

            # For best performance, use num_crops=4 for multi-frame, num_crops=16 for single-frame.
            # If you're running into OOM issues, try num_crops=4
            cls._processor = AutoProcessor.from_pretrained(
                model_id,
                trust_remote_code=True,
                num_crops=4
            )
        # Always return the same in-memory model and processor (singleton behavior)
        return cls._model, cls._processor
