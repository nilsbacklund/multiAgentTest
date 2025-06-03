import warnings
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline


class HoneypotAgent:
    """
    Honeypot agent that simulates responses of a vulnerable shell or API endpoint
    using a local HuggingFace model (default 'Gemma-3.1b'), falling back to 'gpt2'
    if the specified model is not available.
    """
    def __init__(self, model_name: str = "Gemma-3.1b"):
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name, local_files_only=True)
            self.model = AutoModelForCausalLM.from_pretrained(model_name, local_files_only=True)
        except Exception:
            warnings.warn(f"Model '{model_name}' not found locally; attempting fallback to 'gpt2'.")
            try:
                self.tokenizer = AutoTokenizer.from_pretrained("gpt2", local_files_only=True)
                self.model = AutoModelForCausalLM.from_pretrained("gpt2", local_files_only=True)
            except Exception:
                warnings.warn("Fallback model 'gpt2' not found locally; attempting remote download.")
                try:
                    self.tokenizer = AutoTokenizer.from_pretrained("gpt2")
                    self.model = AutoModelForCausalLM.from_pretrained("gpt2")
                except Exception as e:
                    raise RuntimeError("Failed to load fallback model 'gpt2'") from e
        self.generator = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            device=-1,
        )

    def generate_response(self, command: str) -> str:
        """
        Generate a simulated response for the given attacker command.

        Args:
            command (str): The shell or API command from the attacker.

        Returns:
            response (str): Simulated vulnerable system response.
        """
        prompt = (
            f"The attacker runs:\n{command}\n"
            "Respond as a vulnerable system shell or API endpoint."
        )
        result = self.generator(prompt, max_new_tokens=128)[0]["generated_text"]
        return result[len(prompt) :].strip()