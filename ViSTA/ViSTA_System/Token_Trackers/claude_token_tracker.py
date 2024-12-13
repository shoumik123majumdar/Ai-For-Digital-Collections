from token_tracker import TokenTracker

class ClaudeTokenTracker(TokenTracker):
    def update_token_tracker(self,token_data):
        """
        Ability to update all three token counts at once
        :param token_data: usage_metadata object from Gemini API request
        :return:
        """
