import csv
import openai
import json


class SummaryGenerator:
    def __init__(self, openai_api_key):
        self.openai_api_key = openai_api_key

    def read_subtitles_from_csv(self, csv_file_path):
        text = ""
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                text += row[1] + " "
        return text

    def generate_summary(self, text, category):
        openai.api_key = self.openai_api_key

        # Determine the model based on the length of the text
        model = "gpt-3.5-turbo" if len(text.split()) <= 4096 else "gpt-3.5-turbo-16k"
        custom_functions = [
            # Educational Tutorials
            {
                'name': 'extract_educational_summary',
                'description': 'Extract a summary of an educational tutorial from the transcript',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'Title': {'type': 'string', 'description': 'Title of the tutorial'},
                        'Key Points': {'type': 'string', 'description': 'Main teaching points of the tutorial'},
                        'Duration': {'type': 'string', 'description': 'Length of the tutorial'}
                    }
                }
            },
            # Documentary
            {
                'name': 'extract_documentary_summary',
                'description': 'Extract a summary of a documentary from the transcript',
                'parameters': {
                    # Your existing definition
                }
            },
            # Academic Webinar
            {
                'name': 'extract_academic_webinar_summary',
                'description': 'Extract a summary of an academic webinar from the transcript',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'Title': {'type': 'string', 'description': 'Title of the webinar'},
                        'Presenter': {'type': 'string', 'description': 'Name of the presenter'},
                        'Main Topics': {'type': 'string', 'description': 'Key topics discussed in the webinar'}
                    }
                }
            },
            # Podcast Interviews
            {
                'name': 'extract_podcast_summary',
                'description': 'Extract a summary of a podcast interview from the transcript',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'Title': {'type': 'string', 'description': 'Title of the podcast episode'},
                        'Host': {'type': 'string', 'description': 'Name of the host'},
                        'Guest': {'type': 'string', 'description': 'Name of the guest'},
                        'Key Points': {'type': 'string', 'description': 'Main points or topics covered'}
                    }
                }
            },
            # Travel Vlog
            {
                'name': 'extract_travel_vlog_summary',
                'description': 'Extract a summary of a travel vlog from the transcript',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'Title': {'type': 'string', 'description': 'Title of the vlog'},
                        'Destinations': {'type': 'string', 'description': 'Main destinations covered in the vlog'},
                        'Highlights': {'type': 'string', 'description': 'Key highlights or experiences'}
                    }
                }
            },

            # TV Series
            {
                'name': 'extract_tv_series_summary',
                'description': 'Extract a summary of a TV series episode from the transcript',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'Title': {'type': 'string', 'description': 'Title of the episode'},
                        'Season': {'type': 'string', 'description': 'Season number'},
                        'Episode': {'type': 'string', 'description': 'Episode number'},
                        'Plot': {'type': 'string', 'description': 'Brief plot of the episode'}
                    }
                }
            },

            # Gaming
            {
                'name': 'extract_gaming_summary',
                'description': 'Get the gaming summary from the text',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'Title': {'type': 'string', 'description': 'title of the video.'},
                        'Game': {'type': 'string', 'description': 'Name of the game they are streaming'},
                        'Highlights': {'type': 'string', 'description': 'Main highlights or events during the stream'}
                    }
                }
            },

            # Fitness Routine
            {
                'name': 'extract_fitness_routine_summary',
                'description': 'Extract a summary of a fitness routine from the transcript',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'Title': {'type': 'string', 'description': 'Title of the fitness video'},
                        'Routine Type': {'type': 'string', 'description': 'Type of fitness routine'},
                        'Duration': {'type': 'string', 'description': 'Duration of the routine'}
                    }
                }
            },

            # Cooking
            {
                'name': 'extract_cooking_summary',
                'description': 'Extract a summary of a cooking video from the transcript',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'Recipe Name': {'type': 'string', 'description': 'Name of the recipe'},
                        'Ingredients': {'type': 'string', 'description': 'List of main ingredients'},
                        'Cooking Time': {'type': 'string', 'description': 'Total cooking time'}
                    }
                }
            },

            # Science Talks
            {
                'name': 'extract_science_talk_summary',
                'description': 'Extract a summary of a science talk from the transcript',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'Title': {'type': 'string', 'description': 'Title of the talk'},
                        'Speaker': {'type': 'string', 'description': 'Name of the speaker'},
                        'Main Topics': {'type': 'string', 'description': 'Key topics discussed'}
                    }
                }
            },

            # Product Reviews
            {
                'name': 'extract_product_review_summary',
                'description': 'Extract a summary of a product review from the transcript',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'Product Name': {'type': 'string', 'description': 'Name of the product'},
                        'Features': {'type': 'string', 'description': 'Key features of the product'},
                        'Reviewer Opinion': {'type': 'string', 'description': 'Overall opinion of the reviewer'}
                    }
                }
            },

            # Movie Reviews
            {
                'name': 'extract_movie_review_summary',
                'description': 'Extract a summary of a movie review from the transcript',
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'Movie Title': {'type': 'string', 'description': 'Title of the movie'},
                        'Plot': {'type': 'string', 'description': 'Brief plot of the movie'},
                        'Reviewer Rating': {'type': 'integer', 'description': 'Rating given by the reviewer'}
                    }
                }
            }

        ]
        category_function_map = {
          'educational tutorials': 'extract_educational_summary',
          'documentary': 'extract_documentary_summary',
          'academic webinar': 'extract_academic_webinar_summary',
          'podcast interviews': 'extract_podcast_summary',
          'travel vlog': 'extract_travel_vlog_summary',
          'tv series': 'extract_tv_series_summary',
          'gaming': 'extract_gaming_summary',
          'fitness routine': 'extract_fitness_routine_summary',
          'cooking': 'extract_cooking_summary',
          'science talks': 'extract_science_talk_summary',
          'product reviews': 'extract_product_review_summary',
          'movie reviews': 'extract_movie_review_summary'
      }

        function_name = category_function_map.get(category, 'default_summary_function')
        function_obj = next((func for func in custom_functions if func['name'] == function_name), None)
        if function_obj is None:
            raise ValueError(f"No function found for category: {category}")


        description = [text]
        for i in description:
          response = openai.ChatCompletion.create(
              model = 'gpt-3.5-turbo',
              messages = [{'role': 'user', 'content': i}],
              functions = [function_obj],
              function_call = 'auto'
          )

          # Loading the response as a JSON object
          json_response = json.loads(response['choices'][0]['message']['function_call']['arguments'])
          return json_response

    def save_summary_to_file(self, summary, file_path):
      with open(file_path, 'w', encoding='utf-8') as file:
        summary_str = json.dumps(summary, indent=4)  # Convert dict to a formatted string
        file.write(summary_str)

    def create_summary_from_csv(self, csv_file_path, category):
        try:
            print(category)
            subtitles_text = self.read_subtitles_from_csv(csv_file_path)
            summary = self.generate_summary(subtitles_text, category)

            output_file_path = csv_file_path.replace('.csv', '_summary.txt')
            self.save_summary_to_file(summary, output_file_path)

            return output_file_path
        except Exception as e:
            print(f"An error occurred while creating summary: {e}")
            return None