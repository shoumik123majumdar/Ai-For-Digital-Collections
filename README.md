# Vision-Informed Semantic Tagging and Annotator (ViSTA)

This repository is primarily aimed at processing undigitized images from the Digital Repository Service (DRS) at Northeastern University. This project leverages multi-model VLM models (Gemini Pro 1.5, Claude Sonnet/Opus) to tag images with key metadata (ie: titles, abstracts, and subjects), contributing to Northeastern's Digital Repository Archives.

This repository is open for use by anyone interested in metadata tagging and annotation, including but not limited to libraries, archives, and other literary organizations.

The results from all of the research done to implement this system is linked below

**[LINK TO LLM TESTING SPREADSHEET](https://docs.google.com/spreadsheets/d/1R5ee1EAB3jAFGcf7yF1zcKy2gPfhhpjEfJ12hB3jQ3M/edit?usp=sharing)**

**[LINK TO PROJECT REPORT](https://docs.google.com/document/d/1D2Sl5qin717Rd5SLhbf8nJ0PCjrHwAxFPNjmyL1c4vk/edit?usp=sharing)**

**[LINK TO SYSTEM DESIGN PROTOTYPE V1](System_Design_(ROUGHDRAFT).pdf)**

### How It Works
1. **Image Pre-Processing** The system pre-processes images and converts them to `.jpeg` format for VLM use, adjusting quality to optimize for API Image upload constraints. 
2. **Transcription:** Some collections within the DRS (ie: Boston Globe) contain an additional side to each of the digitally stored photographs that possesses additional textual context about the photograph itself. ViSTA is capable of transcribing text off of the additional image to extract 
3. **Title and Abstract Generation:** The script generates descriptive titles and abstracts for the image based on its content as well as additional context.
4. **Tagging**

