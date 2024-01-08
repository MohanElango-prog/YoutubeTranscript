from flask import Flask, request, jsonify
import logging
import sys
import asyncio
import os
import json
from summariser import SummaryGenerator
from transcript import TranscriptExtractor
from classifier import CategoryExtractor

# Initialize logging
logging.basicConfig(level=logging.INFO,
                    stream=sys.stdout,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Create Flask app instance
app = Flask(__name__)


# Synchronous function to process the video
def process_video(youtube_url, my_secret):
  try:
    # Validate YouTube URL
    if "youtube.com" not in youtube_url and "youtu.be" not in youtube_url:
      logging.error("Invalid YouTube URL")
      return None

    # Create a new event loop for running asynchronous code
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    transcript_extractor = TranscriptExtractor()
    # Run the coroutine until it is complete using the event loop
    csv_file = loop.run_until_complete(transcript_extractor.get_transcript(youtube_url))


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
      logging.info(f"Summary Text: {summary_text}")
    return summary_text

  except Exception as e:
    error_message = f"An error occurred: {str(e)}"
    logging.error(error_message)
    return error_message


# Define home route
@app.route("/", methods=["GET"])
def home():
  return jsonify({"message": "Welcome to the Video Processing API"})


# Define route to process video
@app.route("/process_video", methods=["POST"])
def process_video_route():
    data = request.get_json()
    youtube_url = data.get("youtube_url")
    if not youtube_url:
        return jsonify({"error": "No YouTube URL provided"}), 400

    my_secret = os.environ.get('YOUR_OPENAI_KEY')
    if not my_secret:
        return jsonify({"error": "OpenAI key not found"}), 500

    try:
        # Process the video synchronously
        summary_text = process_video(youtube_url, my_secret)
        if summary_text and not summary_text.startswith("An error occurred"):
            json_data = json.loads(summary_text)
            logging.info(f"Returning summary as JSON: {json_data}")
            return jsonify({"success": True, "summary": json_data})
        else:
            # Here, instead of just a generic message, return the error caught from process_video
            return jsonify({"error": "Processing failed. Error: " + str(summary_text) }), 500
    except Exception as e:
        logging.error(f"An exception occurred: {str(e)}")
        return jsonify({"error": "An internal error occurred: " + str(e)}), 500


# Run the app
if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080,
          debug=True)  # Enable debug for development
