import os
import google.generativeai as genai

GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)

for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)

model = genai.GenerativeModel('gemini-pro-vision')

with open('rules.md', 'r') as f:
    rules = f.read()

directory = input('Enter the directory of the file(s): ')

files = os.listdir(directory)

total_text = ''

for file in files:
    if file.endswith('.jpg') or file.endswith('.jpeg'):
        mime_type = 'image/jpeg'
    elif file.endswith('.png'):
        mime_type = 'image/png'
    else:
        print(f'Unsupported file type: {file}')
        continue
    with open(os.path.join(directory, file), 'rb') as f:
        content = f.read()
        image_part = {
            'data': content,
            'mime_type': mime_type
        }
        parts = [
            image_part,
            {
                'text': f"Extract the text from the given image (markdown formatted with math rendering).\n## Rules\n**{rules}**"
            }
        ]
        response = model.generate_content(parts)
        response = ''.join(map(lambda part: part.text, response.candidates[0].content.parts))
        response = response.replace('\\(', '$').replace('\\)', '$')
        print(response)
        total_text += response + '\n'

with open('output.md', 'w', encoding='utf-8') as f:
    f.write(total_text)
