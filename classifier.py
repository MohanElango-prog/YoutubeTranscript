import csv
import openai
import json


class CategoryExtractor:

  def __init__(self, openai_api_key):
    self.openai_api_key = openai_api_key

  def read_subtitles_from_csv(self, csv_file_path):
    text = ""
    max_characters = 4000  # Approximate character count for 500 tokens
    with open(csv_file_path, 'r', encoding='utf-8') as file:
      reader = csv.reader(file)
      next(reader)  # Skip header
      for row in reader:
        text += row[1] + " "
        if len(text) >= max_characters:
          break
    return text

  def classify(self, text):
    openai.api_key = self.openai_api_key
    model = "gpt-3.5-turbo"

    custom_functions = [
        {
            'name': 'extract_Category',
            'description':
            'Extract the one of the following categories from the text, educational tutorials, documentary, academic webinar, podcast interviews, travel vlog, tv series, gaming, fitness routine, cooking, science talks, product reviews, movie reviews.ducational tutorials, documentary, academic webinar, podcast interviews, travel vlog, tv series, gaming, fitness routine, cooking, science talks, product reviews, movie reviews.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'Category': {
                        'type': 'string',
                        'description': 'Category of the Text'
                    },
                }
            }
        },
    ]

    description = [text]
    for i in description:
      response = openai.ChatCompletion.create(model='gpt-3.5-turbo',
                                              messages=[{
                                                  'role': 'user',
                                                  'content': i
                                              }],
                                              functions=custom_functions,
                                              function_call='auto')

      # Loading the response as a JSON object
      # print(response['choices'][0]['message']['function_call']['arguments'])
      json_response = json.loads(
          response['choices'][0]['message']['function_call']['arguments'])
      # print(json_response)
      category_value = json_response.get('Category', 'general')
      return category_value

  def classify_from_csv(self, csv_file_path):
    text = self.read_subtitles_from_csv(csv_file_path)
    if text:
      return self.classify(text)
    else:
      print("No text found in the CSV file.")
      return None
