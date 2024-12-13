from .image_description_model import ImageDescriptionModel
import anthropic
import os


class ClaudeImageDescriptionModel(ImageDescriptionModel):
    """
    Generates Image Descriptions (Titles, Abstracts) using Claude
    """

    def __init__(self, title_prompt_file, abstract_prompt_file, token_tracker):
        super().__init__(title_prompt_file, abstract_prompt_file, token_tracker)
        api_key = os.environ.get("CLAUDE_KEY")
        self.client = anthropic.Anthropic(api_key=api_key)

    def generate_title(self, image_file, context=""):
        """
        """
        title_prompt = self.title_generation_prompt + (context or "")
        content = self._prepare_content(image_file, title_prompt, "title")
        response = self.client.messages.create(
            max_tokens=1500,
            messages=[{"role": "user", "content": content}],
            model='claude-3-5-sonnet-20241022',
        )
        self.token_tracker.update_token_tracker(response.usage)

        title = " ".join([tb.text for tb in response.content]) if isinstance(response.content,
                                                                             list) else response.content
        return title

    def generate_abstract(self, image_file, context=""):
        """
        """
        abstract_prompt = self.abstract_generation_prompt + (context or "")
        content = self._prepare_content(image_file, abstract_prompt, "abstract")
        response = self.client.messages.create(
            max_tokens=1500,
            messages=[{"role": "user", "content": content}],
            model = 'claude-3-5-sonnet-20241022',
        )
        self.token_tracker.update_token_tracker(response.usage)

        # Assuming response.content is a list of TextBlock objects, extract the text from the list
        abstract = " ".join([tb.text for tb in response.content]) if isinstance(response.content,
                                                                                list) else response.content
        return abstract

    def _prepare_content(self, image_file, prompt, task):
        """
        Helper function to prepare content for Claude API request
        """
        content = []

        # add front image content
        content.append({"type": "text", "text": f"Front Image:"})
        content.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/jpeg",
                "data": image_file
            }
        })

        # add task specific prompt
        if task == "title":
            content.append({"type": "text", "text": f"Generate a title based on the following title prompt: {prompt}"})
        elif task == "abstract":
            content.append({"type": "text", "text": f"Generate an abstract based on the following abstract prompt: {prompt}"})

        return content








