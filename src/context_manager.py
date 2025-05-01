from src.utils import anonymize_candidate_info  # Import data anonymization utility


class ContextManager:
    """Manages context based on user's progress through the interview."""

    def __init__(self):
        self.data = {}  # Store candidate info
        self.current_prompt_index = 0  # Track current prompt index
        self.greet = True  # Flag for greeting state
        self.pseudo_name = None  # Store anonymized candidate name
        self.info_order = [  # Order of info to collect
            "full_name",
            "email",
            "phone",
            "experience",
            "position",
            "location",
            "tech_stack"
        ]

    def next_info_prompt(self, PROMPTS):
        """Return the next information gathering prompt."""
        if self.current_prompt_index < len(self.info_order):  # More info to collect
            key = self.info_order[self.current_prompt_index]  # Current info key
            self.current_prompt_index += 1  # Move to next prompt
            return key, PROMPTS["gather_info"][key]  # Return key and prompt text
        else:
            return 'form_completed', None  # All info collected

    def get_tech_stack(self):
        return self.data["tech_stack"]  # Return candidate's tech stack

    def get_candidate_profile(self):
        """Builds a simple candidate profile string."""
        anonymized_data = anonymize_candidate_info(self.data)  # Anonymize data
        name = anonymized_data.get("name", "Unknown")  # Get anonymized name
        self.pseudo_name = name  # Save pseudo name for later use for answer modification
        experience = anonymized_data.get("experience", "Unknown")  # Get experience
        position = anonymized_data.get("position", "Unknown")  # Get position
        return f"{name}, {experience} years experience, interested in {position}"  # Format profile

