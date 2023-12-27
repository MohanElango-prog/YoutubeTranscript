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
          {
              'name': 'extract_educational_summary',
              'description': 'Generate a structured summary with emoji bullet points for educational tutorials',
              'parameters': {
                  'type': 'object',
                  'properties': {
                      'Main Topics': {'type': 'string', 'description': '📚 Main topics covered'},
                      'Key Points': {'type': 'string', 'description': '🔑 Key teaching points or methods explained'},
                  }
              }
          },
          # Documentary
          {
              'name': 'extract_documentary_summary',
              'description': 'Create a structured summary with emoji bullet points for documentaries',
              'parameters': {
                  'type': 'object',
                  'properties': {
                      'Theme': {'type': 'string', 'description': '🌍 Main theme of the documentary'},
                      'Key Facts': {'type': 'string', 'description': '🔎 Key historical or factual points'},
                  }
              }
          },
          # Academic Webinar
          {
              'name': 'extract_academic_webinar_summary',
              'description': 'Summarize academic webinars with structured format and emoji bullets',
              'parameters': {
                  'type': 'object',
                  'properties': {
                      'Topics': {'type': 'string', 'description': '📖 Main topics discussed'},
                      'Insights': {'type': 'string', 'description': '💡 Key insights or findings'},
                  }
              }
          },
          # Podcast Interviews
          {
              'name': 'extract_podcast_summary',
              'description': 'Summarize podcast interviews using emojis and a structured layout',
              'parameters': {
                  'type': 'object',
                  'properties': {
                      'Discussion Points': {'type': 'string', 'description': '🎙️ Key discussion points'},
                      'Quotes': {'type': 'string', 'description': '💬 Notable quotes from the host and guest'},
                  }
              }
          },
          # Travel Vlog
          {
              'name': 'extract_travel_vlog_summary',
              'description': 'Create a travel vlog summary with a structured, emoji-enhanced format',
              'parameters': {
                  'type': 'object',
                  'properties': {
                      'Destinations': {'type': 'string', 'description': '🌏 Main destinations visited'},
                      'Experiences': {'type': 'string', 'description': '🌟 Unique experiences or activities'},
                  }
              }
          },
          # TV Series
          {
              'name': 'extract_tv_series_summary',
              'description': 'Use structured summaries with emojis for TV series episodes',
              'parameters': {
                  'type': 'object',
                  'properties': {
                      'Plot': {'type': 'string', 'description': '📺 Plot of the episode'},
                      'Developments': {'type': 'string', 'description': '🎭 Key characters and developments'},
                  }
              }
          },
          # Gaming
          {
              'name': 'extract_gaming_summary',
              'description': 'Generate a gaming session summary with structured bullet points using emojis',
              'parameters': {
                  'type': 'object',
                  'properties': {
                      'Events': {'type': 'string', 'description': '🎮 Main events of the gaming session'},
                      'Strategies': {'type': 'string', 'description': '🕹️ Key strategies used'},
                  }
              }
          },
          # Fitness Routine
          {
              'name': 'extract_fitness_routine_summary',
              'description': 'Summarize fitness videos using structured format and emojis',
              'parameters': {
                  'type': 'object',
                  'properties': {
                      'Exercises': {'type': 'string', 'description': '💪 Key exercises in the routine'},
                      'Tips': {'type': 'string', 'description': '🏋️ Specific tips or techniques mentioned'},
                  }
              }
          },
          # Cooking
          {
              'name': 'extract_cooking_summary',
              'description': 'Create a cooking video summary with structured, emoji-enhanced format',
              'parameters': {
                  'type': 'object',
                  'properties': {
                      'Recipe': {'type': 'string', 'description': '🍳 Name of the recipe and main ingredients'},
                      'Cooking Steps': {'type': 'string', 'description': '👩‍🍳 Steps involved in cooking'},
                  }
              }
          },
          # Science Talks
          {
              'name': 'extract_science_talk_summary',
              'description': 'Summarize science talks using a structured format and emojis',
              'parameters': {
                  'type': 'object',
                  'properties': {
                      'Concepts': {'type': 'string', 'description': '🔬 Main scientific concepts discussed'},
                      'Findings': {'type': 'string', 'description': '🧪 Key findings or theories'},
                  }
              }
          },
          # Product Reviews
          {
              'name': 'extract_product_review_summary',
              'description': 'Use emojis and structured format for product review summaries',
              'parameters': {
                  'type': 'object',
                  'properties': {
                      'Features': {'type': 'string', 'description': '🛍️ Key features of the product'},
                      'Opinion': {'type': 'string', 'description': '👍 Reviewer\'s overall opinion'},
                  }
              }
          },
          # Movie Reviews
          {
              'name': 'extract_movie_review_summary',
              'description': 'Summarize movie reviews with structured emoji bullets',
              'parameters': {
                  'type': 'object',
                  'properties': {
                      'Plot': {'type': 'string', 'description': '🎥 Brief plot of the movie'},
                      'Rating': {'type': 'string', 'description': '⭐ Reviewer\'s rating of the movie'},
                  }
              }
          },
          # Default/General Summary
          {
              'name': 'default_summary_function',
              'description': 'Generate a general summary with a structured, emoji-enhanced format',
              'parameters': {
                  'type': 'object',
                  'properties': {
                      'Summary': {'type': 'string', 'description': '📝 General summary of the content'}
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