import re
import csv
from youtube_transcript_api import YouTubeTranscriptApi

class TranscriptExtractor:
    def __init__(self):
        pass

    def extract_video_id(self, url):
        regex = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/)([^\s&]+)"
        match = re.search(regex, url)
        return match.group(1) if match else None

    def subtitles_to_csv(self, video_id):
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            transcript = transcript_list.find_transcript(['en'])
            transcript_data = transcript.fetch()

            csv_file_name = f"{video_id}_segments.csv"

            with open(csv_file_name, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Start Time', 'Segment Text'])

                segment_start_time = 0
                segment_text = ""
                segment_duration = 120

                for line in transcript_data:
                    if line['start'] < segment_start_time + segment_duration:
                        segment_text += line['text'] + " "
                    else:
                        writer.writerow([segment_start_time, segment_text.strip()])
                        segment_start_time = line['start']
                        segment_text = line['text'] + " "

                if segment_text:
                    writer.writerow([segment_start_time, segment_text.strip()])

            return csv_file_name
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_transcript(self, url):
        video_id = self.extract_video_id(url)
        if video_id:
            return self.subtitles_to_csv(video_id)
        else:
            print("Invalid YouTube URL")
            return None
