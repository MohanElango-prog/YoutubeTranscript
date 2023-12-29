import csv
import openai
import json


class CategoryExtractor:

  def __init__(self, openai_api_key):
    self.openai_api_key = openai_api_key

  def read_subtitles_from_csv(self, csv_file_path):
    text = "<start of transcript>"
    max_characters = 4000  # Approximate character count for 500 tokens
    with open(csv_file_path, 'r', encoding='utf-8') as file:
      reader = csv.reader(file)
      next(reader)  # Skip header
      for row in reader:
        text += row[1] + " "
        if len(text) >= max_characters:
          break
      text += "<end of transcript>"
    return text

  def classify(self, text):
    openai.api_key = self.openai_api_key
    model = "gpt-3.5-turbo"
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{
            "role":
            "system",
            "content":
            "Classify the above text to any of the following category. The categories are educational tutorials, documentary, podcast interviews, travel vlog, tv series, gaming, fitness routine, cooking, science, product reviews, movie reviews. If none of the category matches make it as general."
        }, {
            "role": "user",
            "content": text
        }, {
            "role": "assistant",
            "content": "Product reviews"
        }],
        temperature=1,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0)
    return response['choices'][0]['message']['content']

  def classify_from_csv(self, csv_file_path):
    text = self.read_subtitles_from_csv(csv_file_path)
    if text:
      return self.classify(text)
    else:
      print("No text found in the CSV file.")
      return None
