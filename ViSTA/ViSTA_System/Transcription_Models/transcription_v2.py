import re


class Transcription():
    """
    Class for storing transcription information
    ie: photographer name, dates, and raw transcription.
    """
    def __init__(self,raw_transcription,detail_extraction):
        self.transcription = raw_transcription
        self.detail_extraction = detail_extraction
        self.name, self.dates = self._extract_details()


    def _extract_details(self):
        """
        Helper method to extract photographer name and date from the detail_extraction field
        :return: photographer name as a string and a list of the dates
        """
        # Extract Name
        name_match = re.search(r'Name:\s*(.*)', self.detail_extraction)
        name = name_match.group(1).strip() if name_match else None

        # Treat "N/A" as None
        if name == "N/A":
            name = None

        # Extract Dates
        dates_match = re.search(r'Date:\s*\[(.*?)\]', self.detail_extraction)
        dates = dates_match.group(1).split(', ') if dates_match else []

        return name, dates

    def extract_names(self):
        """
        Extracts and returns the photographers name from the transcription
        Inputs:
            - None
        Outputs:
            - Returns the photographer name as a string
            OR
            - Returns: "" (makes it easier for MetadataExporter class to compile metadata)
        """
        if self.name is None:
            return ""
        else:
            return self.name

    def extract_dates(self):
        """
        Extracts and returns a list of dates present in the transcription
        Inputs:
            - None
        Outputs:
            - Returns list of dates
            OR
            - Returns "" (makes it easier for MetadataExporter class to compile metadata)
        """
        if len(self.dates) == 0:
            return ""
        else:
            return self.dates
