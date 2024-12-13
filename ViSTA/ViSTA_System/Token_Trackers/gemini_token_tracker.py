from .token_tracker import TokenTracker

class GeminiTokenTracker(TokenTracker):
    def update_token_tracker(self,token_data):
        """
        Ability to update all three token counts at once
        :param token_data: usage_metadata object from Gemini API request
        :return:
        """
        self.update_total_token_count(token_data.total_token_count)
        self.update_total_input_token_count(token_data.prompt_token_count)
        self.update_total_output_token_count(token_data.candidates_token_count)