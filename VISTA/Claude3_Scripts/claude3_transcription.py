import base64
import os
import anthropic

# setup Claude 3 api key
api_key = os.environ.get('API_KEY')


def encode_image(image_path):
    # Encode image to base 64
    with open(image_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def process_image_and_generate_transcription(back_image_path, transcription_prompt):
    """
    This function takes an image path and transcription prompt,
    then it returns the transcription of the back of the image.
    """
    # Encode back image to base 64
    back_image_base64 = encode_image(back_image_path)

    # Claude API request
    client = anthropic.Anthropic(api_key=api_key)

    # Create a combined prompt to describe the image, and generate title and abstract
    response = client.messages.create(
        model='claude-3-opus-20240229',
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Back Image:"
                    },
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",  # You can change this if the image is in another format
                            "data": back_image_base64,
                        },
                    },
                    {
                        "type": "text",
                        "text": f"Generate a transcription based on the following transcription guidelines: {transcription_prompt}"
                    }
                ]
            }
        ],
    )

    # Extract the content from the response
    content = response.content  # Access the response content
    usage = response.usage.input_tokens  # Access token usage

    return content, usage


def load_prompt_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()


# Paths to image and prompts
back_image_path = 'neu_4f1985411.jpg'
transcription_prompt_path = '../transcription_prompt.txt'

# Load the prompt
transcription_prompt = load_prompt_from_file(transcription_prompt_path)

# Process the image and generate the title and abstract
content, total_tokens = process_image_and_generate_transcription(back_image_path, transcription_prompt)

print(f'Generated transcription: \n{content}')
print(f'Total Tokens Used: {total_tokens}')