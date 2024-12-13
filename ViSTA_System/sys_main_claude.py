#!/usr/bin/python
import sys
sys.path.append("/home/ViSTA/ViSTA/ViSTA_System")

from Image_Processors.claude_image_processor import ClaudeImageProcessor
from Transcription_Models.claude_transcription_model import ClaudeTranscriptionModel
from Image_Description_Models.claude_image_description_model import ClaudeImageDescriptionModel
from Metadata_Exporters.metadata_exporter import MetadataExporter
from Metadata_Exporters.metadata import Metadata
from Metadata_Exporters.extended_metadata import ExtendedMetadata
from logger import Logger
from token_tracker import TokenTracker
import pandas as pd
from datetime import datetime


def load_manifest(manifest):
    """
    load the given manifest file
    :param manifest: manifest file (.xlsx)
    :return: manifest file as a DataFrame
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

        if sequence == 1:  # front image
            front_image_path = image_path
        elif sequence == 2:  # back image
            back_image_path = image_path

        # process front-back pair or single front image if it is the last item
        if last_item:
            if back_image_path:
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
        csv_file,
        token_tracker,
        logger,
        log_file_path,
        back_image_path=None
):
    """
    Generates metadata for a single image and writes it to a csv file
    Works with either a single image, or an image_front/back pairing

    :param front_image_path: path to front image
    :param image_processor: ImageProcessor object to process the image
    :param transcription_model: TranscriptionModel object to generate a Transcription
    :param description_model: ImageDescriptionModel object to generate title and abstract
    :param metadata_exporter: MetadataExporter object to write resulting Metadata object to csv file
    :param single_image_csv: csv file for single image metadata
    :param front_back_csv: csv file for front-back image metadata
    :param token_tracker: TokenTracker object to track the tokens used to generate the metadata
    :param back_image_path: Optional parameter that contains the Path to the image back if necessary
    :return:
    """

    process_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    error_message = ""

    try:
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

        # create metadata object
        metadata = Metadata(image_front.display_name, title, abstract, token_tracker)
        if back_image_path:
            metadata = ExtendedMetadata(image_front.display_name, title, abstract, transcription, token_tracker)

        # write metadata to csv
        metadata_exporter.write_to_csv(metadata, csv_file)

        # reset token tracker
        token_tracker.reset()

    except Exception as e:
        # capture error message
        error_message = str(e)
        logger.append_entry(log_file_path, front_image_path, process_start_time,
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S"), error_message)
        raise  # Re-raise the exception after logging

    process_end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Log successful process completion
    if not error_message:
        logger.append_entry(log_file_path, front_image_path, process_start_time, process_end_time, error_message)


def main():
    # Ask for the image_directory they want to process

    """
    image_directory = input("Name of image batch directory uploaded to the efs-dps/input directory that you want to be processed:")
    image_directory = f"efs/home/ec2-user/efs-dps/input/{image_directory}"
    manifest = load_manifest(f"{image_directory}/manifest.xlsx")
    """
    image_batch_name = input(
        "Name of image batch directory uploaded to the test-batches directory that you want to be processed:")
    image_directory = f"efs/home/ec2-user/efs-dps/input/{image_batch_name}"
    manifest = load_manifest(f"{image_directory}/manifest.xlsx")

    # save to csv file
    output_csv = f"{image_batch_name}_claude_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"

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
    vista_logger = Logger('Logs')
    log_file_path = vista_logger.generate_log(f"{output_csv}_log") # ENTER PATH HERE



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
            output_csv,
            token_tracker,
            vista_logger,
            log_file_path,
            back
        )
    )


if __name__ == '__main__':
    main()


