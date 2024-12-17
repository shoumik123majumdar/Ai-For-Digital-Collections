from abc import ABC, abstractmethod
import json
import csv

class MetadataExporter(ABC):
    """
    Class that packages and exports metadata information objects into a variety of formats
    Supports csv and json exports
    """

    def write_to_csv(self, metadata,csv_file):
            """
            Takes metadata object and appends contents to a newly generated csv file located in home/efs-dps/output
            :param metadata: metadata object to be written to csv_file
            :param csv_file: name of the csv_file to be generated
            :return: None: csv file will be altered in place
            """
            with open(f"/home/ec2-user/efs-dps/output/CSV_files/{csv_file}", "a") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(metadata.get_metadata_as_list())

    def jsonify_metadata(self,metadata):
        """
        Takes metadata object and returns it
        :param metadata: metadata object to be converted into JSON
        :return: json: JSON object containing metadata information (not python dictionary)
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
            "total_input_tokens": metadata.get_input_tokens(),
            "total_output_tokens": metadata.get_total_output_tokens()
        }
        return json.dumps(metadata_dict, indent=4)

    def jsonify_extended_metadata(self,extended_metadata):
        """
        Takes extended metadata object and returns it
        :param extended_metadata: ExtendedMetadata object to be written to csv_file
        :return: json: json object containing metadata information (not python dictionary)
        """
        metadata_dict = {
            "image_title": extended_metadata.get_image_title(),
            "title": extended_metadata.get_title(),
            "abstract": extended_metadata.get_abstract(),
            "photographer_name": extended_metadata.get_photographer_name(),
            "primary_date": extended_metadata.get_primary_date(),
            "secondary_date": extended_metadata.get_secondary_date(),
            "transcription": extended_metadata.get_transcription(),
            "total_tokens": extended_metadata.get_total_tokens(),
            "total_input_tokens": extended_metadata.get_input_tokens(),
            "total_output_tokens": extended_metadata.get_total_output_tokens()
        }
        return json.dumps(metadata_dict, indent=4)


