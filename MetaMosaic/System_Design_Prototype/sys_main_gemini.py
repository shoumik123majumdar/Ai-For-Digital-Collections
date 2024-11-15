from gemini_image_processor import GeminiImageProcessor
from gemini_transcription_model import GeminiTranscriptionModel
from gemini_image_description_model import GeminiImageDescriptionModel
from metadata_exporter import MetadataExporter
from metadata import Metadata
from extended_metadata import ExtendedMetadata
from transcription import Transcription
import time

def generate_metadata_front_and_back(image_front,image_back,transcription_model,image_description_model,metadata_exporter,csv_file):
    transcription = transcription_model.generate_transcription(image_back)
    context = transcription.get_raw_transcription()
    total_token_count = transcription_model.get_total_tokens()
    total_input_token_count = transcription_model.get_input_tokens()
    total_output_token_count = transcription_model.get_output_tokens()

    print(total_token_count)
    print(total_input_token_count)
    print(total_output_token_count)

    title = image_description_model.generate_title(image_front,context)
    time.sleep(60) #To bypass the 2 requests per minute limitation set for the free tier of the Gemini API
    abstract = image_description_model.generate_abstract(image_front,context)

    total_token_count +=image_description_model.get_total_tokens()
    total_input_token_count +=image_description_model.get_total_input_tokens()
    total_output_token_count +=image_description_model.get_total_output_tokens()

    print(total_token_count)
    print(total_input_token_count)
    print(total_output_token_count)

    metadata = ExtendedMetadata(image_front.display_name,title,abstract,transcription,total_token_count,total_input_token_count,total_output_token_count)
    metadata_exporter.write_to_csv(metadata,csv_file)

def generate_metadata_single_image(image_front,image_description_model,metadata_exporter,csv_file):
    title = image_description_model.generate_title(image_front,"")
    time.sleep(60)
    abstract = image_description_model.generate_abstract(image_front,"")

    total_token_count = image_description_model.get_total_tokens()
    total_input_token_count = image_description_model.get_total_input_tokens()
    total_output_token_count = image_description_model.get_total_output_tokens()

    metadata = Metadata(image_front.display_name, title, abstract,total_token_count,
                        total_input_token_count, total_output_token_count)
    metadata_exporter.write_to_csv(metadata, csv_file)

result_double_csv = "CSV_files/double_image_results.csv"
result_single_csv = "CSV_files/single_image_results.csv"
image_front_path = "../Test_Images/report_test.jpg"
image_back_path = "../Test_Images/system_test_back.tif"

#Image preprocessing step
image_processor_model = GeminiImageProcessor()
#image_back = image_processor_model.process_image(image_back_path)
image_front = image_processor_model.process_image(image_front_path)

#Initialize transcription model
transcription_prompt_file= "Prompts/Transcription_Prompts/transcription_prompt.txt"
transcription_model = GeminiTranscriptionModel(transcription_prompt_file)
#Make sure in documentation relationship with transcription and photographer_name/date is clear


#Initialize image description model
title_prompt_file = "Prompts/Title_Prompts/title_prompt.txt"
abstract_prompt_file = "Prompts/Abstract_Prompts/abstract_prompt.txt"
image_description_model = GeminiImageDescriptionModel(title_prompt_file, abstract_prompt_file)

#Initialize metadata exporter class
metadata_exporter = MetadataExporter()

#generate_metadata_front_and_back(image_front,image_back,transcription_model,image_description_model,metadata_exporter,result_double_csv)
generate_metadata_single_image(image_front,image_description_model,metadata_exporter,result_single_csv)

#HOW LONG DID THE RUN TAKE?
#TODO: How do I run the code easily for