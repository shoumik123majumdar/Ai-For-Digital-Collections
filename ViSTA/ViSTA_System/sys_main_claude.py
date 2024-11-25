from Image_Processors.claude_image_processor import ClaudeImageProcessor
from Transcription_Models.claude_transcription_model import ClaudeTranscriptionModel
from Image_Description_Models.claude_image_description_model import ClaudeImageDescriptionModel
from Metadata_Exporters.metadata_exporter import MetadataExporter
from Metadata_Exporters.metadata import Metadata
from Metadata_Exporters.extended_metadata import ExtendedMetadata
from Transcription_Models.transcription import Transcription
from token_tracker import TokenTracker
import pandas as pd


def load_manifest(manifest):
    """
    Load the image manifest to a pandas dataframe
    """
    manifest_dataframe = pd.read_excel(manifest)
    manifest_dataframe['Last Item'] = manifest_dataframe['Last Item'].fillna(False).astype(bool)
    return manifest_dataframe


def process_images_from_manifest(manifest, image_directory, generate_metadata):
    """
    Process images from the manifest and handle front-back or front-only cases

    :param manifest (DataFrame): DataFrame containing the manifest data
    :param image_directory: Path to directory containing the images
    :param generate_metadata (function): Function to call to generate metadata
    """
    manifest = manifest.sort_values(by=['File Name', 'Sequence'])

    front_image_path = ""
    back_image_path = None

    for _, row in manifest.iterrows():
        file_name = row['File Name']
        sequence = row['Sequence']
        last_item = row['Last Item']

        # determine the file path
        image_path = f"{image_directory}/{file_name}"

        if sequence == 1: # front image
            front_image_path = image_path
        elif sequence == 2: # back image
            back_image_path = image_path

        # process front-back pair or single front image if it is the last item
        if last_item:
            if back_image_path:
                print("front_image_path")
                print("back_image_path")
                generate_metadata(front_image_path, back_image_path)
                # reset paths for next group
                front_image_path = ""
                back_image_path = ""
            else:
                generate_metadata(front_image_path)
                # reset paths for next group
                front_image_path = ""
                back_image_path = ""


def generate_metadata(
        front_image_path,
        image_processor,
        transcription_model,
        description_model,
        metadata_exporter,
        single_image_csv,
        front_back_csv,
        token_tracker,
        back_image_path=None
):
    """

    :param front_image_path:
    :param image_processor:
    :param transcription_model:
    :param description_model:
    :param metadata_exporter:
    :param single_image_csv:
    :param front_back_csv:
    :param token_tracker:
    :param back_image_path:
    :return:
    """

    # process front image
    image_front = image_processor.process_image(front_image_path)

    # process back image (if any) and generate metadata
    context = None
    transcription = None
    if back_image_path:
        image_back = image_processor.process_image(back_image_path)
        transcription = transcription_model.generate_transcription(image_back)
        context = transcription.transcription

    # generate title and abstract using description model
    title = description_model.generate_title(image_front, context)
    abstract = description_model.generate_abstract(image_front, context)

    # determine single or front-back image
    if back_image_path:
        # save metadata for front-back image pair
        metadata = ExtendedMetadata(
            image_front.display_name,
            title,
            abstract,
            transcription,
            token_tracker
        )
        metadata_exporter.write_to_csv(metadata, front_back_csv)
    else:
        # save metadata for single image
        metadata = Metadata(
            image_front.display_name,
            title,
            abstract,
            token_tracker
        )
        metadata_exporter.write_to_csv(metadata, single_image_csv)

    # reset token tracker
    token_tracker.reset()


def main():
    # paths to manifest and image directory
    manifest = load_manifest("../test-batches/fronts_samples/manifest.xlsx")
    image_directory = "../test-batches/fronts_samples"

    # paths to prompts
    transcription_prompt = "Prompts/Transcription_Prompts/transcription_step_one.txt"
    detail_extraction_prompt_file = "Prompts/Transcription_Prompts/transcription_step_two.txt"
    title_prompt_file = "Prompts/Title_Prompts/title_prompt.txt"
    abstract_prompt_file = "Prompts/Abstract_Prompts/abstract_prompt.txt"

    # initialize models
    token_tracker = TokenTracker()
    image_processor = ClaudeImageProcessor
    transcription_model = ClaudeTranscriptionModel(transcription_prompt, detail_extraction_prompt_file, token_tracker)
    image_description_model = ClaudeImageDescriptionModel(title_prompt_file, abstract_prompt_file, token_tracker)
    metadata_exporter = MetadataExporter()

    # save to csv file
    result_single_csv = "CSV_files/claude_front_sample_test.csv"
    result_front_back_csv = "CSV_files/claude_front-back_sample_test.csv"

    # process images from manifest
    process_images_from_manifest(
        manifest,
        image_directory,
        lambda front, back=None: generate_metadata(
            front,
            image_processor,
            transcription_model,
            image_description_model,
            metadata_exporter,
            result_single_csv,
            result_front_back_csv,
            back
        )
    )


if __name__ == '__main__':
    main()


