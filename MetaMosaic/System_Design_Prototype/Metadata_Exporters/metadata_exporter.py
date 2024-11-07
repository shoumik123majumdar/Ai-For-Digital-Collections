from abc import ABC, abstractmethod
import json

class MetadataExporter(ABC):
    """
    Class that packages and exports metadata information objects into a variety of formats
    Supports csv and json exports
    """

    def write_to_csv(self, metadata,csv_file_path):
        """
        Takes metadata object and appends contents to the csv file located @ csv_file_path
        :param metadata: metadata object to be written to csv_file
        :param csv_file_path: csv file path to the csv that the metadata will be appended into
        :return: None: csv file will be altered in place
        """
        with open(csv_file_path, "a") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(metadata.get_metadata_as_list())

    def jsonify_metadata(self,metadata,csv_file_path):
        """
        Takes metadata list object and returns it
        :param metadata_dict: metadata to be written to csv_file
        :param csv_file_path: csv file path to the csv that the metadata will be written into
        :return: json: json object containing metadata information (not python dictionary)
        """
        metadata_dict = {
            "image_title": metadata.get_image_title(),
            "title": metadata.get_title(),
            "abstract": metadata.get_abstract(),
            "photographer_name": metadata.get_photographer_name(),
            "primary_date": metadata.get_primary_date(),
            "secondary_date": metadata.get_secondary_date(),
            "transcription": metadata.get_transcription(),
            "total_tokens": metadata.get_total_tokens(),
            "total_input_tokens": metadata.get_total_input_tokens(),
            "total_output_tokens": metadata.get_total_output_tokens()
        }
        return json.dumps(metadata_dict, indent=4)

