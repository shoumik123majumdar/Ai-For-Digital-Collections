from Image_Processors.gemini_image_processor import GeminiImageProcessor
from Transcription_Models.gemini_transcription_model import GeminiTranscriptionModel
from Image_Description_Models.gemini_image_description_model import GeminiImageDescriptionModel
from Metadata_Exporters.metadata_exporter import MetadataExporter
from Metadata_Exporters.metadata import Metadata
from Metadata_Exporters.extended_metadata import ExtendedMetadata
from Transcription_Models.transcription import Transcription
from token_tracker import TokenTracker
import time

def generate_metadata_single_image(image_front_path,image_processor,image_description_model,metadata_exporter,csv_file,token_tracker):
    image_front = image_processor.process_image(image_front_path)

    title = image_description_model.generate_title(image_front,"")
    abstract = image_description_model.generate_abstract(image_front,"")

    metadata = Metadata(image_front.display_name, title, abstract,token_tracker)
    metadata_exporter.write_to_csv(metadata, csv_file)

    #reset token counting mechanism after every metadata object generated
    token_tracker.reset()

def generate_metadata_front_and_back(image_front_path,image_back_path,image_processor,transcription_model,image_description_model,metadata_exporter,csv_file,token_tracker):
    image_front = image_processor.process_image(image_front_path)
    image_back = image_processor.process_image(image_back_path)

    transcription = transcription_model.generate_transcription(image_back)
    context = transcription.transcription

    time.sleep(60)
    title = image_description_model.generate_title(image_front,context)
     #To bypass the 2 requests per minute limitation set for the free tier of the Gemini API
    time.sleep(30)
    abstract = image_description_model.generate_abstract(image_front,context)

    metadata = ExtendedMetadata(image_front.display_name,title,abstract,transcription,token_tracker)
    metadata_exporter.write_to_csv(metadata,csv_file)

    token_tracker.reset()

#Initialize image_processor
image_processor = GeminiImageProcessor()

#Initialize token tracker class
token_tracker = TokenTracker()

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
image_front_path = "../Test_Images/portrait.tif"
image_back_path = "../Test_Images/portrait_back.tif"
result_double_csv = "CSV_files/double_image_results.csv"
result_single_csv = "CSV_files/single_image_results.csv"

generate_metadata_front_and_back(image_front_path,image_back_path,image_processor,transcription_model,image_description_model,metadata_exporter,result_double_csv,token_tracker)
#generate_metadata_single_image(image_front_path,image_processor,image_description_model,metadata_exporter,result_single_csv,token_tracker)


""" Be able to mix and match
Directory_Path = "Images"
with open("manifest.txt",'r') as manifest_file:
    file_name = manifest_file.read()
    image_front_path - f"{Directory_Path}{file_name}"
    generate_metadat


Directory:
for identifier in directory:
    generate_metadata_front_and_back(image):
"""
