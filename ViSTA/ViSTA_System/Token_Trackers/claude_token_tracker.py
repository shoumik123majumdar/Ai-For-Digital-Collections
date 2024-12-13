from .token_tracker import TokenTracker

class ClaudeTokenTracker(TokenTracker):
    def update_token_tracker(self,token_data):
        """
        Ability to update all three token counts at once
        :param token_data: usage_metadata object from Gemini API request
        :return:
        """
        # Extract token data from the response
        total_tokens = token_data.get("total_tokens")
        input_tokens = token_data.get("input_tokens")
        output_tokens = token_data.get("output_tokens")

        # Update token counts
        self.update_total_token_count(total_tokens)
        self.update_total_input_token_count(input_tokens)
        self.update_total_output_token_count(output_tokens)
