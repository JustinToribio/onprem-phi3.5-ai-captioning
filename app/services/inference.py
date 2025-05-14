from app.models.phi3_model import Phi3Model

def run_caption_inference(image, user_prompt, model_id, max_tokens, test_mode=False, verbose=False):
    model, processor = Phi3Model.load(model_id, test_mode=test_mode)

    # Offical docs on the inference code below: https://huggingface.co/microsoft/Phi-3.5-vision-instruct

    # Construct chat-like message structure expected by the model
    messages = [{
        "role": "user",
        "content": "<|image_1|>\n" + user_prompt
    }]

    # Convert messages to a raw prompt string
    prompt = processor.tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )

    # Process the prompts and images
    inputs = processor(prompt, [image], return_tensors="pt").to("cuda")

    # Define generation parameters
    # do_sample: False - Picks the token with the highest probability (greedy decoding). Temperature does nothing when this is False.
    # do_sample: True - Samples from the probability distribution (based on temperature, top_k, top_p, etc.)
    # temperature: (float, only works if do_sample: True) 0.0 - Greedy and deterministic (always picks the most likely next token)
    # temperature: ~0.7 - Balanced creativity and coherence (default for many models)
    # temperature: >1.0 - High randomness and creativity (can get chaotic or incoherent)
    # If you're running into OOM issues, reduce max_new_tokens
    generation_args = {
        "max_new_tokens": 100 if verbose else 10 if test_mode else max_tokens,
        "do_sample": False
    }

    # Generate output token ID's from the inputs
    generate_ids = model.generate(
        **inputs,
        eos_token_id=processor.tokenizer.eos_token_id,
        **generation_args
    )

    # Remove the input token IDs from the generated IDs
    generate_ids = generate_ids[:, inputs['input_ids'].shape[1]:]

    # Decode the generated token IDs to text
    response = processor.batch_decode(
        generate_ids, skip_special_tokens=True
    )[0]

    return response
