from image_description_model import ImageDescriptionModel
import google.generativeai as genai
import os

class GeminiImageDescriptionModel(ImageDescriptionModel):
    """
    Generates Image Descriptions (Titles, Abstracts) using Gemini
    """
    def __init__(self, title_prompt_file,abstract_prompt_file):
        super().__init__(title_prompt_file,abstract_prompt_file)
        goog_key = os.environ.get("GOOG_KEY")
        genai.configure(api_key=goog_key)
        generation_config = genai.GenerationConfig(temperature=0)
        self.__model = genai.GenerativeModel("gemini-1.5-pro", generation_config=generation_config)

    def _generate_content(self, prompt, image_file):
        """
        Helper method that refactors some of the code in generate_title and generate_abstract
        :param prompt: prompt you would like to be included in the API request
        :param image_file: image_file you would like to include in the API request
        :return: returns API response text and usage_metadata
        """
        response = self.__model.generate_content(contents=[prompt, image_file])
        return response.text, response.usage_metadata

    def generate_title(self, image_file, context=""):
        title_prompt = self.title_generation_prompt + context
        self.title_token_data = self._generate_content(title_prompt, image_file)[1]
        return self._generate_content(title_prompt, image_file)[0]

    def generate_abstract(self, image_file, context=""):
        abstract_prompt = self.abstract_generation_prompt + context
        self.abstract_token_data = self._generate_content(abstract_prompt, image_file)[1]
        return self._generate_content(abstract_prompt, image_file)[0]

    def get_total_tokens(self):
        if self.abstract_token_data is None or self.title_token_data is None:
            return "abstract or title has not been generated yet, therefore no total token count can be returned"
        else:
            return self.title_token_data.total_token_count + self.abstract_token_data.total_token_count

    def get_total_input_tokens(self):
        if self.abstract_token_data is None or self.title_token_data is None:
            return "abstract or title has not been generated yet, therefore no total token count can be returned"
        else:
            return self.title_token_data.prompt_token_count + self.abstract_token_data.prompt_token_count

    def get_total_output_tokens(self):
        if self.abstract_token_data is None or self.title_token_data is None:
            return "abstract or title has not been generated yet, therefore no total token count can be returned"
        else:
            return self.title_token_data.candidates_token_count + self.abstract_token_data.candidates_token_count