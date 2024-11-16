import base64
import os
import anthropic

# setup Claude 3 api key
api_key = os.environ.get('API_KEY')


def encode_image(image_path):
    # Encode image to base 64
    with open(image_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def process_image_and_generate_titles(front_image_path, back_image_path, title_prompt):
    """
    This function takes an image path and title prompt,
    then it returns the generated title for the image.
    """

    # Encode front and back images to base 64
    front_image_base64 = encode_image(front_image_path) if front_image_path else None
    back_image_base64 = encode_image(back_image_path) if back_image_path else None

    # Claude API request
    client = anthropic.Anthropic(api_key=api_key)

    # create a prompt to generate titles for the front and back images if provided
    content = []
    if front_image_base64:
        content.append({"type": "text", "text": "Front Image:"})
        content.append({"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": front_image_base64}})

    if back_image_base64:
        content.append({"type": "text", "text": "Back Image:"})
        content.append({"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": back_image_base64}})

    # add the prompt for title generation
    content.append({"type": "text", "text": f"Generate a title based on the following title prompt: {title_prompt}"})

    response = client.messages.create(
        model='',
        max_tokens=1054,
        messages=[{"role": "user", "content": content}]
    )

    # extract the content from the response
    content = response.content
    usage = response.usage.input_tokens

    return content, usage


def load_prompt_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()


# paths to images and title prompt
front_image_path = 'path/to/front_image.jpg'
back_image_path = 'path/to/back_image.jpg'
title_prompt_path = 'title_prompt.txt'

# load title prompt
title_prompt = load_prompt_from_file(title_prompt_path)

# process the image and generate titles
title, total_tokens = process_image_and_generate_titles(front_image_path, back_image_path, title_prompt)

print(f'Generated Title: \n{title}')
print(f'Total Tokens Used: {total_tokens}')