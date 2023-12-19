from transcript import TranscriptExtractor
from summariser import SummaryGenerator
import os


def main():
  my_secret = os.environ['YOUR_OPENAI_KEY']

  # Prompt the user for the YouTube URL
  youtube_url = input("Please enter the YouTube video URL: ")
  openai_api_key = my_secret

  # Your OpenAI API key

  # Instance of the TranscriptExtractor class from transcript.py
  transcript_extractor = TranscriptExtractor()
  csv_file = transcript_extractor.get_transcript(youtube_url)

  if csv_file:
    print(f"Transcript saved to CSV file: {csv_file}")

    # Instance of the SummaryGenerator class from summariser.py
    summary_generator = SummaryGenerator(openai_api_key)
    summary_file = summary_generator.create_summary_from_csv(csv_file)

    if summary_file:
      print(f"Summary saved to file: {summary_file}")
    else:
      print("Failed to generate summary.")
  else:
    print("Failed to extract transcript.")


if __name__ == "__main__":
  main()
