#!/usr/bin/python
import sys
sys.path.append("/home/ViSTA/ViSTA/ViSTA_System")


from Image_Processors.gemini_image_processor import GeminiImageProcessor
from Transcription_Models.gemini_transcription_model import GeminiTranscriptionModel
from Image_Description_Models.gemini_image_description_model import GeminiImageDescriptionModel
from Metadata_Exporters.metadata_exporter import MetadataExporter
from Metadata_Exporters.metadata import Metadata
from Metadata_Exporters.extended_metadata import ExtendedMetadata
from logger import Logger
from token_tracker import TokenTracker
import pandas as pd
from datetime import datetime


def load_manifest(manifest):
    """
    Load the given manifest file
    :param manifest: manifest file.xlsx
    :return: manifest file as a DataFrame
    """
    manifest_dataframe = pd.read_excel(manifest)
    manifest_dataframe['Last Item'] = manifest_dataframe['Last Item'].fillna(False).astype(bool)
    return manifest_dataframe

def process_manifest_images(manifest,image_directory, generate_metadata):
    """
    Process images from a manifest file.
    Handles front-back and front-only cases.
    :param manifest (DataFrame): DataFrame containing the manifest file
    :param image_directory: Path to the directory containing the images
    :param generate_metadata: Lambda function to generate the metadata
    :return: N/A. Once processed, all metadata will be exported to a csv file
    """

    manifest = manifest.sort_values(by=['File Name', 'Sequence'])

    front_image_path = ""
    back_image_path = None

    for _, row in manifest.iterrows():
        file_name = row['File Name']
        sequence = row['Sequence']
        last_item = row['Last Item']

        image_path = f"{image_directory}/{file_name}"

        if sequence == 1:  # front image
            front_image_path = image_path
        elif sequence == 2:  # back image
            back_image_path = image_path


        # process front-back pair or single front image if it is the last item
        if last_item:
            if back_image_path:
                generate_metadata(front_image_path,back_image_path)
                # reset paths for next group
                front_image_path = ""
                back_image_path = ""
            else:
                generate_metadata(front_image_path)
                # reset paths for next group
                front_image_path = ""
                back_image_path = ""

def generate_metadata(image_front_path,image_processor,transcription_model,image_description_model,metadata_exporter,csv_file,token_tracker,logger,log_file_path,image_back_path=None):
    """
    Generates metadata for a single image and writes it to a csv file
    Works with either a single image, or an image_front/back pairing
    :param image_front_path: path to the image
    :param image_processor: ImageProcessor object to process image @ image_front_path
    :param transcription_model: TranscriptionModel object to generate a Transcription (object)
    :param image_description_model: ImageDescriptionModel object to generate title and abstract
    :param metadata_exporter: MetadataExporter object to write resulting Metadata object to csv file
    :param csv_file: The csv file you want to append the Metadata to
    :param token_tracker: TokenTracker object to track the tokens used to generate the metadata
    :param logger: Logger object to log the start/end times of each run through
    :param log_file_path: path to the log file
    :param image_back_path: Optional parameter that contains the Path to the image back if necessary
    :return: N/A. Results are written to a csv file
    """
    process_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    error_message = ""

    try:
        # Process front image
        image_front = image_processor.process_image(image_front_path)
        context = ""
        transcription = None

        # Process back image and transcription if provided
        if image_back_path:
            image_back = image_processor.process_image(image_back_path)
            transcription = transcription_model.generate_transcription(image_back)
            context = transcription.transcription

        # Generate title and abstract
        title = image_description_model.generate_title(image_front, context)
        abstract = image_description_model.generate_abstract(image_front, context)

        # Create Metadata object
        metadata = Metadata(image_front.display_name, title, abstract, token_tracker)
        if image_back_path:
            metadata = ExtendedMetadata(image_front.display_name, title, abstract, transcription, token_tracker)

        # Write metadata to CSV
        metadata_exporter.write_to_csv(metadata, csv_file)

        # Reset token tracker
        token_tracker.reset()

    except Exception as e:
        # Capture error message
        error_message = str(e)
        logger.append_entry(log_file_path, image_front_path, process_start_time,
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S"), error_message)
        raise  # Re-raise the exception after logging

    process_end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Log successful process completion
    if not error_message:
        logger.append_entry(log_file_path, image_front_path, process_start_time, process_end_time, error_message)


def main():

    manifest = load_manifest("../efs-dps/fronts_samples/manifest.xlsx")
    image_directory = "../efs-dps/fronts_samples"

    """
    manifest = load_manifest("../test-batches/fronts-backs_samples/manifest.xlsx")
    image_directory = "../test-batches/fronts-backs_samples"
    #result_csv = "CSV_files/fronts_gemini_test.csv"
     """

    """
    GENERATE OWN CSV FILE
    """
    result_csv = input("Name of .csv file to write metadata to:")
    result_csv_path = f'CSV_files/{result_csv}'
    #Initialize image_processor
    image_processor = GeminiImageProcessor()

    #Initialize token tracker class
    token_tracker = TokenTracker()

    #Initialize logger and generate a log
    ViSTA_logger = Logger('Logs')
    log_file_path = ViSTA_logger.generate_log(f'{result_csv}_log') #<----- ENTER PATH HERE


    #Initialize transcription model
    transcription_prompt_file= "Prompts/Transcription_Prompts/transcription_step_one.txt"
    detail_extraction_prompt_file = "Prompts/Transcription_Prompts/transcription_step_two.txt"
    transcription_model = GeminiTranscriptionModel(transcription_prompt_file,detail_extraction_prompt_file,token_tracker)


    #Initialize image description model
    title_prompt_file = "Prompts/Title_Prompts/title_prompt.txt"
    abstract_prompt_file = "Prompts/Abstract_Prompts/abstract_prompt.txt"
    image_description_model = GeminiImageDescriptionModel(title_prompt_file, abstract_prompt_file,token_tracker)

    #Initialize metadata exporter class
    metadata_exporter = MetadataExporter()

    #ACTUAL PROCESSING CODE AFTER MODEL INSTANTIATION
    process_manifest_images(
        manifest,
        image_directory,
        lambda front, back=None: generate_metadata(
            front, image_processor, transcription_model, image_description_model, metadata_exporter, result_csv_path  ,token_tracker, ViSTA_logger, log_file_path,back
        )
    )

if __name__ == '__main__':
    main()



#Prompt for csv file name
#Prompt for log file name

#Do not judge based on word order judge based on level of phrases
#Keyword ground truth

