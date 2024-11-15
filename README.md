# AI for Digital Collections: Vision-Informed Semantic Tagging and Annotator (ViSTA)

This is a research-focused repository aimed at processing undigitized images from the Digital Repository at Northeastern University. This project leverages multi-model models (Google Gemini, Claude Sonnet/Opus) and their computer vision and large language model (VLM) capabilities to generate key metadata (ie: titles, abstracts, and subjects) for images, contributing to Northeastern's Digital Repository Archives.

This project is currently in the research phase but is planned for future integration into the Northeastern Digital Repository Services pipeline.

**[LINK TO LLM TESTING SPREADSHEET](https://docs.google.com/spreadsheets/d/1R5ee1EAB3jAFGcf7yF1zcKy2gPfhhpjEfJ12hB3jQ3M/edit?usp=sharing)**

**[LINK TO PROJECT REPORT](https://docs.google.com/document/d/1D2Sl5qin717Rd5SLhbf8nJ0PCjrHwAxFPNjmyL1c4vk/edit?usp=sharing)**

**[LINK TO SYSTEM DESIGN PROTOTYPE V1](System_Design_(ROUGHDRAFT).pdf)**

### How It Works

1. **Image Pre-Processing** The system pre-processes images and converts them to `.jpeg` format for VLM use, adjusting quality to optimize for API Image upload constraints. 
2. **Transcription:** (IF Back-ImageCapable of transcribing text off of images for additional context
3. **Detail Extraction:** Key metadata like photographer name, dates, and raw transcription is extracted from the generated text.
4. **Title Generation:** The script generates a descriptive title for the image based on its content and extracted metadata.
5. **Abstract Generation:** Finally, an abstract is generated to summarize the context and content of the image.


