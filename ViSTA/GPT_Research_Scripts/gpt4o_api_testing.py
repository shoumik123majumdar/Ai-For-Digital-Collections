import base64
import requests
import os

# setup openai api key
api_key = os.environ.get('API_KEY')

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def get_image_description(image_path):
    """
    Analyze the image and return a description using ChatGPT vision

    :param image_path: Path to image file
    :return: Description of image
    """

    # encode the image to base 64
    base64_image = encode_image(image_path)

    # prepare headers and payload for API request
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        'model': "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What's in this image?"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
    }

    # Make the request to OpenAPI api
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    # parse the response and return the description
    return response.json()['choices'][0]['message']['content'], response.json()['usage']['total_tokens']


def load_prompt_from_file(file_path):
    """
    Extract prompt from prompt file
    :param file_path: path to txt file
    :return: extracted text
    """
    with open(file_path, 'r') as file:
        return file.read().strip()


def generate_image_descriptions(front_image_description, title_prompt, abstract_prompt, back_image_description=None):
    """
    Generate title, abstract, and subjects based on the image description and guidelines

    :param front_image_description: description of front of the image
    :param title_prompt: guidelines for generating titles
    :param abstract_prompt: guidelines for generating abstracts
    :param back_image_description: description of back of image if available
    :return: Generated title, abstract, and subjects
    """

    if back_image_description:
        combined_description = f"Front: {front_image_description}. Back:{back_image_description}"
    else:
        combined_description = f"Front: {front_image_description}"

    response = requests.post(
        url="https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": f"As a library catalogger, you are tasked with generating a title for the input. Use the following guidelines: {title_prompt}"},
                {"role": "user", "content": f"Description: {combined_description}. Please provide a title."},
                {"role": "system", "content": f"As a library catalogger, you are tasked with generating an abstract for the input. Use the following guidelines: {abstract_prompt}"},
                {"role": "user", "content": f"Description: {combined_description}. Please provide an abstract and subjects (or keywords)."}
            ],
        }
    )

    return response.json()['choices'][0]['message']['content'], response.json()['usage']['total_tokens']


# paths
front_image_path = '/Users/rahuldmello/Desktop/Co-op/AI_testing/GPT4_testing/neu_m0449024q.jpg'
back_image_path = '/Users/rahuldmello/Desktop/Co-op/AI_testing/GPT4_testing/neu_m04490268.jpg'
title_prompt_path = '../abstract_prompt.txt'
abstract_prompt_path = '../abstract_prompt.txt'

# load the prompts from the files
title_prompt = load_prompt_from_file(title_prompt_path)
abstract_prompt = load_prompt_from_file(abstract_prompt_path)

# extract info from front of image
front_image_description, front_image_tokens = get_image_description(front_image_path)

# optionally extract image description for back of image
back_image_description = None
back_image_tokens = 0
if os.path.exists(back_image_path):
    back_image_description, back_image_tokens = get_image_description(back_image_path)

# generate title, abstract, and subjects
metadata, metadata_tokens = generate_image_descriptions(front_image_description, title_prompt, abstract_prompt, back_image_description)

# calculate total tokens
total_tokens = front_image_tokens + back_image_tokens + metadata_tokens

print(f'Image Description: {front_image_description}')
if back_image_description:
    print(f"Back Image Description: {back_image_description}")
print(f'Generated Metadata: \n{metadata}')
print(f'Total Tokens Used: {total_tokens}')



