import os
import pandas as pd
import claude3_titles
import claude3_abstracts
import claude3_transcription

# setup paths to images and csv
image_dir = 'path to images'
output_csv = 'claude3_compiled_image_metadata.csv'

# initialize an empty list for data
data = []

# function to process image and compile information
def process_image(image_filename):
    """
    Processes an image through title, abstract, and transcription methods,
    and returns the compiled information.
    """

    # paths to title, abstract, and transcription prompts
    title_prompt_path = '.../title_prompt.txt'
    abstract_prompt_path = '.../abstract_prompt.txt'
    transcription_prompt_path = '.../transcription_prompt.txt'

    # load prompts
    title_prompt = claude3_titles.load_prompt_from_file(title_prompt_path)
    abstract_prompt = claude3_abstracts.load_prompt_from_file(abstract_prompt_path)
    transcription_prompt = claude3_transcription.load_prompt_from_file(transcription_prompt_path)

    # paths to front and back images
    front_image_path = os.path.join(image_dir, image_filename)
    back_image_path = os.path.join(image_dir, image_filename.replace('_front', '_back'))

    # generate title
    title, _ = claude3_titles.process_image_and_generate_titles(front_image_path, back_image_path, title_prompt)

    # generate abstract
    abstract, _ = claude3_abstracts.process_image_and_generate_abstracts(front_image_path, back_image_path, abstract_prompt)

    # generate transcription
    transcription, _ = claude3_transcription.process_image_and_generate_transcription(back_image_path, transcription_prompt)

    # extract photographer name and dates
    photographer_name = extract_photographer_name(transcription)
    dates = extract_dates(transcription)

    # return the compiled row for the CSV
    return {
        "Image Title": image_filename,
        "Title": title.strip(),
        "Abstract": abstract.strip(),
        "Photographer Name": photographer_name.strip(),
        "Dates": dates.strip()
    }

# helper functions to extract photographer name and dates
def extract_photographer_name(transcription):
    """
    Extracts the photographer name from the transcription.
    """
    # assuming transcription has photographer 'name'
    if 'Name:' in transcription:
        return transcription.split('Name:')[1].split('\n')[0].strip()
    return 'N/A'


def extract_dates(transcription):
    """
    Extracts the dates from the transcription.
    """
    # assuming transcription has 'Date'
    if 'Date:' in transcription:
        return transcription.split('Date:')[1].split('\n')[0].strip()
    return 'N/A'


# process each image and compile the data
for image_filename in os.listdir(image_dir):
    if image_filename.endswith("_front.jpg"):
        img_data = process_image(image_filename)
        data.append(img_data)

# create pandas dataframe
df = pd.DataFrame(data)

# save the dataframe to a CSV
df.to_csv(output_csv, index=False)

