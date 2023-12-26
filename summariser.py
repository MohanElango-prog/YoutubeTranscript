import csv
import openai

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

    def generate_summary(self, text):
        openai.api_key = self.openai_api_key

        # Determine the model based on the length of the text
        model = "gpt-3.5-turbo" if len(text.split()) <= 4096 else "gpt-3.5-turbo-16k"

        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "Summarise the following subtitles into engaging form. You can use emoji as bulletins whenever necessary. Keep the summary short and concise."
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            temperature=1,
            max_tokens=500,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response['choices'][0]['message']['content']

    def save_summary_to_file(self, summary, file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(summary)

    def create_summary_from_csv(self, csv_file_path):
        try:
            subtitles_text = self.read_subtitles_from_csv(csv_file_path)
            summary = self.generate_summary(subtitles_text)

            output_file_path = csv_file_path.replace('.csv', '_summary.txt')
            self.save_summary_to_file(summary, output_file_path)

            return output_file_path
        except Exception as e:
            print(f"An error occurred while creating summary: {e}")
            return None