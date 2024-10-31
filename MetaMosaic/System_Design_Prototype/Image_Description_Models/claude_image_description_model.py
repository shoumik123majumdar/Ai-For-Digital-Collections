from image_description_model import ImageDescriptionModel
import anthropic
import os


class ClaudeImageDescriptionModel(ImageDescriptionModel):
    """
    Generates Image Descriptions (Titles, Abstracts) using Claude
    """

    def __init__(self, image_file, context=None):
        super().__init__(image_file)
        api_key = os.environ.get("CLAUDE_API_KEY")
        self.client = anthropic.Anthropic(api_key=api_key)
        self.context = context
        self.title_token_data = None
        self.abstract_token_data = None

    def generate_title(self):
        """
        """
        content = self._prepare_content(self.title_generation_prompt, "title")
        response = self.client.messages.create(
            model='claude-3-5-sonnet-20241022',
            messages=[{"role": "user", "content": content}]
        )
        self.title_token_data = response.usage
        return response.content

    def generate_abstract(self):
        """
        """
        content = self._prepare_content(self.abstract_generation_prompt, "abstract")
        response = self.client.messages.create(
            model = 'claude-3-5-sonnet-20241022',
            messages=[{"role": "user", "content": content}]
        )
        self.abstract_token_data = response.usage
        return response.content

    def _prepare_content(self, prompt, task):
        """
        Helper function to prepare content for Claude API request
        """

        content = []

        # add front image content
        content.append({"type": "text", "text": "Front Image:"})
        content.append({"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": self.image_file}})

        # add context if available
        if self.context:
            content.append({"type": "text", "text": f"Context from Back Image: {self.context}"})

        # add task specific prompt
        if task == "title":
            content.append({"type": "text", "text": f"Generate a title based on the following title prompt: {prompt}"})
        elif task == "abstract":
            content.append({"type": "text", "text": f"Generate an abstract based on the following abstract prompt: {prompt}"})

        return content

    def get_total_tokens(self):
        """
        Returns the total tokens used for generating title and abstract
        """
        if self.abstract_token_data is None or self.title_token_data is None:
            return "Abstract or title has not been generated yet, so no total count can be returned."
        return self.title_token_data['total_tokens'] + self.abstract_token_data['total_tokens']

    def get_total_input_tokens(self):
        """
        Returns the total input tokens used for generating title and abstract
        """
        if self.abstract_token_data is None or self.title_token_data is None:
            return "Abstract or title has not been generated yet, so no total count can be returned."
        return self.title_token_data['prompt_tokens'] + self.abstract_token_data['prompt_tokens']

    def get_total_output_tokens(self):
        """
        Returns the total input tokens used for generating title and abstract
        """
        if self.abstract_token_data is None or self.title_token_data is None:
            return "Abstract or title has not been generated yet, so no total count can be returned."
        return self.title_token_data['completion_tokens'] + self.abstract_token_data['completion_tokens']







