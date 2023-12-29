from flask import Flask, request, jsonify
import asyncio
import logging
import os
from summariser import SummaryGenerator
from transcript import TranscriptExtractor
from classifier import CategoryExtractor

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
app = Flask(__name__)
async def process_video(youtube_url, my_secret):
  try:
    # Validate YouTube URL
    if "youtube.com" not in youtube_url and "youtu.be" not in youtube_url:
      logging.error("Invalid YouTube URL")
      return None

    # Transcript extraction
    transcript_extractor = TranscriptExtractor()
    csv_file = await transcript_extractor.get_transcript(youtube_url)

    if not csv_file:
      logging.error("Failed to extract transcript.")
      return None

    logging.info(f"Transcript saved to CSV file: {csv_file}")

    # Transcript classification
    transcript_classifier = CategoryExtractor(my_secret)
    category = transcript_classifier.classify_from_csv(csv_file)
    if not category:
      logging.error("Failed to classify transcript.")
      return None

    logging.info(f"Transcript classified as: {category}")

    # Summary generation
    summary_generator = SummaryGenerator(my_secret)
    summary_file = summary_generator.create_summary_from_csv(
        csv_file, category)
    if not summary_file:
      logging.error("Failed to generate summary.")
      return None

    logging.info(f"Summary saved to file: {summary_file}")

    # Read the summary file
    with open(summary_file, 'r') as file:
      summary_text = file.read()

    return summary_text

  except Exception as e:
    logging.error(f"An error occurred: {str(e)}")
    return None


@app.route('/process_video', methods=['POST'])
def process_video_route():
  data = request.json
  youtube_url = data.get("youtube_url")
  if not youtube_url:
    return jsonify({"error": "No YouTube URL provided"}), 400

  my_secret = os.environ.get('YOUR_OPENAI_KEY')
  if not my_secret:
    return jsonify({"error": "OpenAI key not found"}), 500

  # Use asyncio to run the async function
  loop = asyncio.new_event_loop()
  asyncio.set_event_loop(loop)
  summary_text = loop.run_until_complete(process_video(youtube_url, my_secret))
  loop.close()

  if summary_text:
    return jsonify({"success": True, "summary": summary_text})
  else:
    return jsonify({"error": "Processing failed"}), 500

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080)
