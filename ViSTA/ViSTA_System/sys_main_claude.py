import pandas as pd
from pathlib import Path
from claude_image_processor import ClaudeImageProcessor
from claude_transcription_model import ClaudeTranscriptionModel
from claude_image_description_model import ClaudeImageDescriptionModel
from metadata_exporter import MetadataExporter
from metadata import Metadata
from extended_metadata import ExtendedMetadata
from transcription import Transcription
import time


def load_manifest(manifest_path):
    """
    Load the image manifest to a pandas dataframe
    """
    return pd.read_excel(manifest_path)

def process_images_from_manifest(manifest, image_directory, generate_metadata):
    """
    Process images from the manifest and handle front-back or front-only cases

    :param manifest (DataFrame): DataFrame containing the manifest data
    :param image_directory: Path to directory containing the images
    :param generate_metadata (function): Function to call to generate metadata
    """
    manifest = manifest.sort_values(by=['File Name', 'Sequence'])

    front_image_path = None
    back_image_path = None

    for _, row in manifest.iterrows():
        file_name = row['File Name']
        sequence = row['Sequence']
        last_item = row['Last Item']

        # determine the file path
        image_path = Path(image_directory) / file_name

        if sequence == 1: # front image
            front_image_path = image_path
        elif sequence == 2: # back image
            back_image_path = image_path

        # process front-back pair or single front image if it is the last item
        if last_item == "TRUE":
            generate_metadata(front_image_path, back_image_path)
            # reset paths for next group
            front_image_path = None
            back_image_path = None


def generate_metadata(front_image_path, image_processor, transcription_model, description_model, metadata_exporter, csv_file, back_image_path=None ):
    """
    Generates metadata for given images

    :param front_image_path: Path to front image
    :param image_processor: Pre-initialized image processor
    :param transcription_model: Pre-initialized Transcription model
    :param description_model: Pre-initialized Description model
    :param metadata_exporter: Pre-initialized Metadata Exporter for exporting metadata
    :param csv_file: Path to csv file
    :param back_image_path: Path to back image (if any)
    :return:
    """

    print(f"Processing images:")
    print(f"Front Image: {front_image_path}")
    if back_image_path:
        print(f"Back Image: {back_image_path}")

    # process front image
    front_image_data = image_processor.process_image(front_image_path)

    # process back image (if any) and generate metadata
    context = None
    if back_image_path:
        back_image_data = image_processor.process_image(back_image_path)
        transcription = transcription_model.generate_transcription(back_image_data)
        context = transcription.get_raw_transcription()
        total_token_count = transcription_model.get_total_tokens()
        total_input_token_count = transcription_model.get_input_tokens()
        total_output_token_count = transcription_model.get_output_tokens()
    else:
        back_image_data = None

    # generate title and abstract using description model
    title = description_model.generate_title(front_image_data, context)
    abstract = description_model.generate_abstract(front_image_data, context)

    total_token_count += description_model.get_total_tokens()
    total_input_token_count += description_model.get_total_input_tokens()
    total_output_token_count += description_model.get_total_output_tokens()

    print(total_token_count)
    print(total_input_token_count)
    print(total_output_token_count)

    # Export metadata
    metadata = ExtendedMetadata(
        file_name=front_image_path.name,
        title=title,
        abstract=abstract,
        transcription=transcription,
        total_token_count=total_token_count,
        total_input_token_count=total_input_token_count,
        total_output_token_count=total_output_token_count
    )

    # write to csv
    metadata_exporter.write_to_csv(metadata, csv_file)

def main():
    # paths to manifest and image directory
    manifest_path = ""
    image_directory = ""

    # paths to prompts
    transcription_prompt = "../deprecated_transcription_prompt.txt"
    title_prompt_file = "../title_prompt.txt"
    abstract_prompt_file = "../abstract_prompt.txt"


    # load manifest
    manifest = load_manifest()

    # initialize models
    image_processor = ClaudeImageProcessor
    transcription_model = ClaudeTranscriptionModel(transcription_prompt)
    image_description_model = ClaudeImageDescriptionModel(title_prompt_file, abstract_prompt_file)
    metadata_exporter = MetadataExporter()

    # process images from manifest
    process_images_from_manifest(
        manifest,
        image_directory,
        lambda front, back: generate_metadata(
            front, image_processor, transcription_model, image_description_model, metadata_exporter, "", back
        )
    )

if __name__ == '__main__':
    main()


#def generate_metadata_front_and_back(image_front,image_back,transcription_model,image_description_model,metadata_exporter,csv_file):
    #transcription = transcription_model.generate_transcription(image_back)
    #context = transcription.get_raw_transcription()
    #total_token_count = transcription_model.get_total_tokens()
    #total_input_token_count = transcription_model.get_input_tokens()
    #total_output_token_count = transcription_model.get_output_tokens()

    #print(total_token_count)
    #print(total_input_token_count)
    #print(total_output_token_count)

    #title = image_description_model.generate_title(image_front,context)
    #time.sleep(60)
    #abstract = image_description_model.generate_abstract(image_front,context)

    #total_token_count += image_description_model.get_total_tokens()
    #total_input_token_count += image_description_model.get_total_input_tokens()
    #total_output_token_count += image_description_model.get_total_output_tokens()

    #print(total_token_count)
    #print(total_input_token_count)
   # print(total_output_token_count)

  #  metadata = ExtendedMetadata(image_front.display_name,title,abstract,transcription,total_token_count,total_input_token_count,total_output_token_count)
 #   metadata_exporter.write_to_csv(metadata,csv_file)


#def generate_metadata_single_image(image_front,image_description_model,metadata_exporter,csv_file):
    #title = image_description_model.generate_title(image_front,"")
    #abstract = image_description_model.generate_abstract(image_front,"")

    #total_token_count = image_description_model.get_total_tokens()
    #total_input_token_count = image_description_model.get_total_input_tokens()
    #total_output_token_count = image_description_model.get_total_output_tokens()

  #  metadata = Metadata(image_front.display_name, title, abstract,total_token_count,
   #                     total_input_token_count, total_output_token_count)
 #   metadata_exporter.write_to_csv(metadata, csv_file)


#result_double_csv = "CSV_files/double_image_results.csv"
#result_single_csv = "CSV_files/fronts_samples_test_1.csv"
#image_front_path = "../Test_Images/system_test_front.tif"
#image_back_path = "../Test_Images/system_test_back.tif"

# Image preprocessing step
#image_processor_model = ClaudeImageProcessor()
#image_back = image_processor_model.process_image(image_back_path)
#image_front = image_processor_model.process_image(image_front_path)

# Initialize transcription model
#transcription_prompt = "../deprecated_transcription_prompt.txt"
#transcription_model = ClaudeTranscriptionModel(transcription_prompt)

# Initialize image description model
#title_prompt_file = "../title_prompt.txt"
#abstract_prompt_file = "../abstract_prompt.txt"
#image_description_model = ClaudeImageDescriptionModel(title_prompt_file, abstract_prompt_file)

#Initialize metadata exporter class
#metadata_exporter = MetadataExporter()

#generate_metadata_front_and_back(image_front,image_back,transcription_model,image_description_model,metadata_exporter,result_double_csv)
#generate_metadata_single_image(image_front,image_description_model,metadata_exporter,result_single_csv)