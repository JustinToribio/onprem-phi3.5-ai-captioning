from transformers import AutoModelForCausalLM, AutoProcessor
import gc
import torch

# Offical docs on the inference code below: https://huggingface.co/microsoft/Phi-3.5-vision-instruct

class Phi3Model:
    # Class-level (shared) variables to store model and processor
    # When the model and processor are loaded for the first time, they'll be stored here
    _model = None
    _processor = None
    _model_id = None

    # Allow method to be called without instantiating the class
    @classmethod
    def load(cls, model_id: str, test_mode=False):
        # If not already loaded, load the model and processor once
        # Model and artifacts are downloaded to ~/.cache/huggingface
        if cls._model is None or cls._processor is None or cls._model_id != model_id:
            print("loading model and processor...")
            cls._model_id = model_id
            cls._model = AutoModelForCausalLM.from_pretrained(
                cls._model_id,
                device_map="cuda",               # Load model onto GPU
                trust_remote_code=True,           # Enable custom model class
                torch_dtype="auto",              # Use optimal precision (e.g. bf16)
                _attn_implementation="eager"      # Fallback for non-flash attention environments
            )

            # For best performance, use num_crops=4 for multi-frame, num_crops=16 for single-frame.
            # If you're running into OOM issues, try num_crops=4
            cls._processor = AutoProcessor.from_pretrained(
                cls._model_id,
                trust_remote_code=True,
                num_crops=2 if test_mode else 4,  # Use 2 crops for faster inference in test mode
            )
            print("model and processor loaded.")
        # Always return the same in-memory model and processor (singleton behavior)
        return cls._model, cls._processor
    
    @classmethod
    def unload(cls):
        if cls._model is not None or cls._processor is not None:
            # Unload model and processor from memory
            print("Unloading model and processor from memory...")
            del cls._model
            del cls._processor
            cls._model = None
            cls._processor = None

            # Force garbage collection
            gc.collect()

            # Clear GPU memory (if CUDA is available)
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                torch.cuda.ipc_collect()
            print("Resources released.")
