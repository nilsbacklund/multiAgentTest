import warnings
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline


class AttackerAgent:
    """
    Attacker agent that generates offensive commands emulating MITRE ATT&CK phases
    using a local HuggingFace model (default 'WhiteRabbitNeo'), falling back to 'gpt2'
    if the specified model is not available.
    """
    def __init__(self, model_name: str = "WhiteRabbitNeo"):
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
        self.phases = [
            "reconnaissance",
            "initial access",
            "privilege escalation",
            "persistence",
            "exfiltration",
        ]
        self.current_phase = 0

    def generate_command(self) -> tuple[str, str]:
        """
        Generate the next shell or API command based on the current attack phase.

        Returns:
            phase (str): MITRE ATT&CK phase label.
            command (str): Generated command string.
        """
        phase = self.phases[self.current_phase]
        prompt = (
            f"You are a red-team attacker performing {phase}. "
            "Provide the next shell or API command to further the objective."
        )
        result = self.generator(
            prompt,
            max_new_tokens=64,
            do_sample=True,
            temperature=0.7,
        )[0]["generated_text"]
        # Strip the prompt prefix to isolate the command
        command = result[len(prompt) :].strip()
        self.current_phase = min(self.current_phase + 1, len(self.phases) - 1)
        return phase, command