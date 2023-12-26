import re
import csv
import logging
import asyncio
from youtube_transcript_api import YouTubeTranscriptApi

class TranscriptExtractor:
    def __init__(self):
        pass

    async def extract_video_id(self, url):
        regex = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/)([^\s&]+)"
        match = re.search(regex, url)
        return match.group(1) if match else None

    async def subtitles_to_csv(self, video_id):
        try:
            transcript_list = await asyncio.get_event_loop().run_in_executor(
                None, YouTubeTranscriptApi.list_transcripts, video_id
            )
            transcript = transcript_list.find_transcript(['en'])
            transcript_data = await asyncio.get_event_loop().run_in_executor(
                None, transcript.fetch
            )

            csv_file_name = f"{video_id}_segments.csv"
            chunk_duration = 120  # 120 seconds (2 minutes)

            with open(csv_file_name, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Start Time', 'Segment Text'])

                chunk_start = 0
                chunk_text = ""

                for line in transcript_data:
                    if line['start'] < chunk_start + chunk_duration:
                        chunk_text += line['text'] + " "
                    else:
                        writer.writerow([chunk_start, chunk_text.strip()])
                        chunk_start = line['start']
                        chunk_text = line['text'] + " "

                # Write the last chunk if there's remaining text
                if chunk_text:
                    writer.writerow([chunk_start, chunk_text.strip()])

            logging.info(f"Transcript data written to {csv_file_name}")
            return csv_file_name
        except Exception as e:
            logging.exception(f"An error occurred while extracting subtitles: {e}")
            return None

    async def get_transcript(self, url):
        try:
            video_id = await self.extract_video_id(url)
            if video_id:
                return await self.subtitles_to_csv(video_id)
            else:
                logging.error("Invalid YouTube URL")
                return None
        except Exception as e:
            logging.exception(f"An error occurred in get_transcript: {e}")
            return None
