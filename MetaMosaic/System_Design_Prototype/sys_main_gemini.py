
"""
Image_front
Image_back

#Preprocessing
ImageProcessorModel
#process Image_Back
image_back = ImageProcessorModel.process_image(image_back)
#process Image_Front
image_front = ImageProcessorModel.process_image(image_front)

TranscriptionModel
ImageDescriptionModel
MetadataExporter


Loop through images
    total_token_count = 0
    total_input_token_count = 0
    total_output_token_count = 0

    transcription = TranscriptionModel.generate_transcription()
    total_token_count += TranscriptionModel.get_total_tokens()
    total_input_token_count += TranscriptionModel.get_total_input_tokens()
    total_output_token_count += TranscriptionModel.get_total_output_tokens()

    title = ImageDescriptionModel.generate_title(image_front,transcription.get_raw())
    abstract = ImageDescriptionModel.generate_abstract(image_front,transcription.get_raw())

    #Total of 1750 input tokens
"""


#Logs
#How long it took
#Total Num token costs