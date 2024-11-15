import re


class Transcription():
    """
    Class for storing transcription information
    ie: photographer name, dates, and raw transcription.
    """
    def __init__(self,transcription):
        self.transcription = transcription
        self.name,self.dates,self.raw = self._extract_details()

    def _extract_details(self):
        """
        Helper method that extracts the photographer name, dates and the raw transcription from self.transcription
        Inputs:
            - N/A
        Outputs:
            - name: photographer name
            - dates: date(s)
            - raw_text: raw transcription
        """
        name_match = re.search(r'Name:(.*)', self.transcription)
        name = name_match.group(1).strip() if name_match else None

        dates_match = re.search(r'Date:\[(.*?)\]', self.transcription)
        dates = dates_match.group(1).split(', ') if dates_match else []

        raw_match = re.search(r'Raw:(.*)', self.transcription, re.DOTALL)
        raw_text = raw_match.group(1).strip() if raw_match else None

        return name, dates, raw_text

    def extract_names(self):
        """
        Extracts and returns the photographers name from the raw_transcription
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
        Extracts and returns a list of dates present in the raw_transcription
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

    def get_raw_transcription(self):
        """
        Gets the raw transcription that was initialized during object creation (self.transcription) and returns it
        Inputs:
            - None
        Outputs:
            - Returns self.transcription as the raw transcription
        """
        return self.raw