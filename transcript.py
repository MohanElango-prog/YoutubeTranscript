import re
import csv
import logging
import asyncio
import math
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled

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

            # Try to get the 'en' transcript, or search for 'en-' as fallback
            try:
                transcript = transcript_list.find_transcript(['en'])
            except NoTranscriptFound:
                en_transcripts = [t for t in transcript_list if t.language_code.startswith('en-')]
                if not en_transcripts:
                    raise NoTranscriptFound(video_id, ['en'])
                transcript = en_transcripts[0]

            transcript_data = await asyncio.get_event_loop().run_in_executor(
                None, transcript.fetch
            )

            csv_file_name = f"{video_id}_segments.csv"
            chunk_duration = 20  # chunk duration changed to 20 seconds

            with open(csv_file_name, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Start Time', 'End Time', 'Segment Text'])

                chunk_start = 0
                chunk_text = ""

                for line in transcript_data:
                    if line['start'] < chunk_start + chunk_duration:
                        chunk_text += line['text'] + " "
                    else:
                        end_time = chunk_start + chunk_duration
                        start_time_formatted = self.format_time(chunk_start)
                        end_time_formatted = self.format_time(end_time)
                        writer.writerow([start_time_formatted, end_time_formatted, chunk_text.strip()])

                        chunk_start = end_time
                        chunk_text = line['text'] + " "

                # Write the last chunk if there's remaining text
                if chunk_text:
                    end_time = chunk_start + chunk_duration
                    start_time_formatted = self.format_time(chunk_start)
                    end_time_formatted = self.format_time(end_time)
                    writer.writerow([start_time_formatted, end_time_formatted, chunk_text.strip()])

            logging.info(f"Transcript data written to {csv_file_name}")
            return csv_file_name
        except TranscriptsDisabled:
            logging.error(f"Transcripts are disabled for video: {video_id}")
            return None
        except NoTranscriptFound:
            logging.error(f"No transcript found for the video with id: {video_id}")
            return None
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

    def format_time(self, time):
        # Helper function to format the time as hh:mm:ss
        hours, remainder = divmod(time, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f'{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}'