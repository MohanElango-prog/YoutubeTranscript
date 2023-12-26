import asyncio
import logging
import os
from summariser import SummaryGenerator
from transcript import TranscriptExtractor
from classifier import CategoryExtractor

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def main():
    try:
        my_secret = os.environ.get('YOUR_OPENAI_KEY')
        if not my_secret:
            logging.error("OpenAI key not found in environment variables.")
            return

        youtube_url = input("Please enter the YouTube video URL: ")

        # Validate YouTube URL
        if "youtube.com" not in youtube_url and "youtu.be" not in youtube_url:
            logging.error("Invalid YouTube URL")
            return

        # Transcript extraction
        transcript_extractor = TranscriptExtractor()
        csv_file = await transcript_extractor.get_transcript(youtube_url)

        if csv_file:
            logging.info(f"Transcript saved to CSV file: {csv_file}")

            # Transcript classification
            transcript_classifier = CategoryExtractor(my_secret)
            category = transcript_classifier.classify_from_csv(csv_file)
            logging.info(f"Transcript classified as: {category}")

            # Summary generation
            summary_generator = SummaryGenerator(my_secret)
            summary_file = summary_generator.create_summary_from_csv(csv_file, category) # Assuming create_summary_from_csv is modified

            if summary_file:
                logging.info(f"Summary saved to file: {summary_file}")
            else:
                logging.error("Failed to generate summary.")
        else:
            logging.error("Failed to extract transcript.")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
