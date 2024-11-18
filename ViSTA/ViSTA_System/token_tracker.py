class TokenTracker:
    """
    Tracks token usage for API calls
    """
    def __init__(self):
        self.total_tokens = 0
        self.input_tokens = 0
        self.output_tokens = 0

    def update_total_token_count(self,total_tokens):
        """
        Adds the given number of total_tokens from a new API request to the existing total_token count
        :param total_tokens: total tokens
        :return: None
        """
        self.total_tokens += total_tokens

    def update_total_input_token_count(self,input_tokens):
        """
        Adds the given number of input_tokens from a new API request to the existing input_token count
        :param input_tokens: input_tokens from API request
        :return: None
        """
        self.input_tokens += input_tokens

    def update_total_output_token_count(self,output_tokens):
        """
        Adds the given number of output_tokens from a new API request to the existing output_token count
        :param output_tokens: output_tokens from API request
        :return: None
        """
        self.output_tokens += output_tokens

    def update_token_tracker(self,token_data):
        """
        Ability to update all three token counts at once
        :param token_data: usage_metadata object from API request
        :return:
        """
        self.update_total_token_count(token_data.total_token_count)
        self.update_total_input_token_count(token_data.prompt_token_count)
        self.update_total_output_token_count(token_data.candidates_token_count)

    def reset(self):
        """
        Resets the token counts to 0
        :return: None
        """
        self.total_tokens = 0
        self.input_tokens = 0
        self.output_tokens = 0