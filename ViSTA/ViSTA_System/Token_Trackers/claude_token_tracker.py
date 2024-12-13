from .token_tracker import TokenTracker

class ClaudeTokenTracker(TokenTracker):

    def update_token_tracker(self,token_data):
        """
        Ability to update all three token counts at once
        :param token_data: usage_metadata object from Gemini API request
        :return:
        """
        # Extract token data from the response
        input_tokens = token_data["input_tokens"]
        output_tokens = token_data["output_tokens"]
        total_tokens = input+output_tokens

        # Update token counts
        self.update_total_token_count(total_tokens)
        self.update_total_input_token_count(input_tokens)
        self.update_total_output_token_count(output_tokens)
