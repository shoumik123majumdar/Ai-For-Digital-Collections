from gemini_image_processor import GeminiImageProcessor
from gemini_transcription_model import GeminiTranscriptionModel
from gemini_image_description_model import GeminiImageDescriptionModel
from metadata_exporter import MetadataExporter
from metadata import Metadata
from transcription import Transcription

def generate_metadata(image_front,transcription_model,image_description_model,metadata_exporter,image_back=""):
    total_token_count = 0
    total_input_token_count = 0
    total_output_token_count = 0
    context = ""
    photographer_name = ""
    dates = ""

    if image_back != "":
        transcription = transcription_model.generate_transcription(image_back)
        context = transcription.get_raw_transcription()
        photographer_name = transcription.get_photographer_name()
        dates = transcription.get_dates()
        total_token_count += tanscription_model.get_total_tokens()
        total_input_token_count += tanscription_model.get_total_input_tokens()
        total_output_token_count += tanscription_model.get_total_output_tokens()


    title = image_description_model.generate_title(image_front,context)
    abstract = image_description_model.generate_abstract(image_front,context)
    total_token_count+=image_description_model.get_total_tokens()
    total_input_token_count+=image_description_model.get_total_input_tokens()
    total_output_token_count+=image_description_model.get_total_output_tokens()

    #ASK CHAT HOW TO GET THE FILE NAME FROM image_front
    metadata = Metadata(image_front,title,abstract,transcription,total_tokens,total_input_tokens,total_output_tokens)
    metadata_exporter.write_to_csv(metadata)

result_csv = "test_system.csv"
image_front_path = "../Test_Images/large.tif"
image_back_path = "../Test_Images/large_back.tif"

#Image preprocessing step
image_processor_model = GeminiImageProcessor()
image_back = image_processor_model.process_image(image_back_path)
image_front = image_processor_model.process_image(image_front_path)

#Initialize transcription model
transcription_prompt = "../transcription_prompt.txt"
transcription_model = GeminiTranscriptionModel(transcription_prompt)

#Initialize image description model
title_prompt_file = "../Test_Images/title_prompt.txt"
abstract_prompt_file = "../Test_Images/abstract_prompt.txt"
image_description_model = GeminiImageDescriptionModel(title_prompt_file, abstract_prompt_file)

#Initialize metadata exporter class
metadata_exporter = MetadataExporter()
generate_metadata(image_front,transcription_model,image_description_model,metadata_exporter,image_back)


#HOW LONG DID THE RUN TAKE?