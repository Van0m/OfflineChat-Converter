from flask import Flask, request, render_template_string

app = Flask(__name__)

def convert_string_to_phonetic(input_string):
    suffix = "uh"
    
    mapping = {
        'i': 'iuh',
        'a': 'auh',
        'o': 'ouh',
    }

    words = input_string.lower().split()
    converted_words = []
    
    for word in words:
        converted_letters = []
        for letter in word:
            if letter in mapping:
                converted_letters.append(mapping[letter])
            elif 'a' <= letter <= 'z':
                converted_letters.append(letter + suffix)
            else:
                converted_letters.append(letter)
        
        converted_words.append(" ".join(converted_letters))
    
    return " ".join(converted_words)

def reverse_phonetic_string(input_string):
    reverse_mapping = {
        'iuh': 'i',
        'auh': 'a',
        'ouh': 'o',
    }
    
    words = input_string.split(' ')
    original_words = []
    
    current_word = []
    for part in words:
        if part in reverse_mapping:
            current_word.append(reverse_mapping[part])
        elif part.endswith('uh') and len(part) > 2:
            current_word.append(part[:-2])
        else:
            if current_word:
                original_words.append("".join(current_word))
            current_word = []
            original_words.append(part)

    if current_word:
        original_words.append("".join(current_word))

    return " ".join(original_words).strip()


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Phonetic String Converter</title>
    <style>
        body {
            font-family: sans-serif;
            background-color: #f4f4f9;
            color: #333;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            padding: 20px;
            box-sizing: border-box;
        }
        .container {
            background-color: #fff;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 600px;
            text-align: center;
        }
        h1 {
            color: #4a4a4a;
            margin-bottom: 20px;
        }
        form {
            margin-bottom: 20px;
        }
        input[type="text"] {
            width: 80%;
            padding: 12px;
            border: 2px solid #ccc;
            border-radius: 8px;
            font-size: 16px;
            margin-right: 10px;
            transition: border-color 0.3s;
        }
        input[type="text"]:focus {
            border-color: #007bff;
            outline: none;
        }
        button {
            padding: 12px 20px;
            border: none;
            background-color: #007bff;
            color: #fff;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s, transform 0.1s;
        }
        button:hover {
            background-color: #0056b3;
        }
        button:active {
            transform: scale(0.98);
        }
        .result-box {
            background-color: #e9ecef;
            border: 1px dashed #adb5bd;
            padding: 20px;
            margin-top: 20px;
            border-radius: 8px;
            word-wrap: break-word;
            text-align: left;
        }
        .result-box h3 {
            margin-top: 0;
            color: #6c757d;
        }
        .copy-btn {
            background-color: #28a745;
            margin-top: 10px;
        }
        .copy-btn:hover {
            background-color: #218838;
        }
        .message {
            margin-top: 10px;
            font-size: 14px;
            color: #007bff;
            display: none;
        }
        hr {
            border: 0;
            height: 1px;
            background: #ccc;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Phonetic String Converter</h1>
        <p>Convert a string to its phonetic version.</p>
        <form action="/" method="post">
            <input type="text" id="input_string" name="input_string" value="{{ input_string | default('', true) }}" placeholder="e.g., I am typing this">
            <button type="submit">Convert</button>
        </form>
        
        {% if converted_string %}
            <div class="result-box">
                <h3>Original:</h3>
                <p>{{ input_string }}</p>
                <h3>Converted:</h3>
                <p id="converted-text">{{ converted_string }}</p>
                <button class="copy-btn" onclick="copyToClipboard()">Copy to Clipboard</button>
                <p id="message" class="message">Copied!</p>
            </div>
        {% endif %}

        <hr>

        <p>Reverse a phonetic string to its original form.</p>
        <form action="/reverse" method="post">
            <input type="text" id="reverse_input_string" name="reverse_input_string" value="{{ reverse_input_string | default('', true) }}" placeholder="e.g., iuh auh muh yuh puh iuh nuh guh">
            <button type="submit">Reverse</button>
        </form>

        {% if reversed_string %}
            <div class="result-box">
                <h3>Phonetic:</h3>
                <p>{{ reverse_input_string }}</p>
                <h3>Original:</h3>
                <p>{{ reversed_string }}</p>
            </div>
        {% endif %}
    </div>

    <script>
        function copyToClipboard() {
            var convertedText = document.getElementById("converted-text").innerText;
            var tempInput = document.createElement("input");
            document.body.appendChild(tempInput);
            tempInput.value = convertedText;
            tempInput.select();
            document.execCommand("copy");
            document.body.removeChild(tempInput);
            
            var messageElement = document.getElementById("message");
            messageElement.style.display = "block";
            setTimeout(function() {
                messageElement.style.display = "none";
            }, 2000);
        }
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    input_text = ""
    converted_text = ""
    
    if request.method == 'POST':
        input_text = request.form.get('input_string', '')
        converted_text = convert_string_to_phonetic(input_text)
        
    return render_template_string(
        HTML_TEMPLATE,
        input_string=input_text,
        converted_string=converted_text
    )

@app.route('/reverse', methods=['GET', 'POST'])
def reverse():
    reverse_input_text = ""
    reversed_text = ""
    
    if request.method == 'POST':
        reverse_input_text = request.form.get('reverse_input_string', '')
        reversed_text = reverse_phonetic_string(reverse_input_text)
        
    return render_template_string(
        HTML_TEMPLATE,
        reverse_input_string=reverse_input_text,
        reversed_string=reversed_text
    )

if __name__ == '__main__':
    app.run(debug=True)

