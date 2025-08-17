from flask import Flask, request, render_template_string, redirect, url_for

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
<html lang="en" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Phonetic String Converter</title>
    <style>
        :root {
            --light-bg: #f4f4f9;
            --light-text: #333;
            --light-container-bg: #fff;
            --light-heading: #4a4a4a;
            --light-result-box-bg: #e9ecef;
            --light-result-box-border: #adb5bd;
            --light-copy-btn: #28a745;
            --light-copy-btn-hover: #218838;
            --light-hr: #ccc;

            --dark-bg: #121212;
            --dark-text: #e0e0e0;
            --dark-container-bg: #1e1e1e;
            --dark-heading: #bb86fc;
            --dark-result-box-bg: #2d2d2d;
            --dark-result-box-border: #444;
            --dark-copy-btn: #03dac6;
            --dark-copy-btn-hover: #018786;
            --dark-hr: #444;
        }

        /* Use the data-theme attribute on the html element for styling */
        html[data-theme="light"] {
            background-color: var(--light-bg);
            color: var(--light-text);
        }

        html[data-theme="dark"] {
            background-color: var(--dark-bg);
            color: var(--dark-text);
        }
        
        body {
            font-family: sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            padding: 20px;
            box-sizing: border-box;
            transition: background-color 0.3s, color 0.3s;
        }
        
        .container {
            background-color: var(--light-container-bg);
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 600px;
            text-align: center;
            transition: background-color 0.3s, box-shadow 0.3s;
        }

        html[data-theme="dark"] .container {
            background-color: var(--dark-container-bg);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
        }

        h1 {
            color: var(--light-heading);
            margin-bottom: 20px;
            transition: color 0.3s;
        }
        html[data-theme="dark"] h1 {
            color: var(--dark-heading);
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
        html[data-theme="dark"] input[type="text"] {
            background-color: #333;
            color: var(--dark-text);
            border-color: #555;
        }

        input[type="text"]:focus {
            border-color: #007bff;
            outline: none;
        }
        html[data-theme="dark"] input[type="text"]:focus {
            border-color: var(--dark-heading);
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
            background-color: var(--light-result-box-bg);
            border: 1px dashed var(--light-result-box-border);
            padding: 20px;
            margin-top: 20px;
            border-radius: 8px;
            word-wrap: break-word;
            text-align: left;
            transition: background-color 0.3s, border-color 0.3s;
        }
        html[data-theme="dark"] .result-box {
            background-color: var(--dark-result-box-bg);
            border: 1px dashed var(--dark-result-box-border);
        }

        .result-box h3 {
            margin-top: 0;
            color: #6c757d;
            transition: color 0.3s;
        }
        html[data-theme="dark"] .result-box h3 {
            color: var(--dark-text);
        }
        
        .copy-btn {
            background-color: var(--light-copy-btn);
            margin-top: 10px;
            transition: background-color 0.3s;
        }
        .copy-btn:hover {
            background-color: var(--light-copy-btn-hover);
        }
        html[data-theme="dark"] .copy-btn {
            background-color: var(--dark-copy-btn);
        }
        html[data-theme="dark"] .copy-btn:hover {
            background-color: var(--dark-copy-btn-hover);
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
            background: var(--light-hr);
            margin: 20px 0;
            transition: background 0.3s;
        }
        html[data-theme="dark"] hr {
            background: var(--dark-hr);
        }

        .theme-toggle {
            position: absolute;
            top: 20px;
            right: 20px;
            display: flex;
            align-items: center;
        }
        .theme-toggle input {
            display: none;
        }
        .theme-toggle label {
            width: 48px;
            height: 24px;
            background-color: #ccc;
            border-radius: 12px;
            position: relative;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .theme-toggle input:checked + label {
            background-color: #555;
        }
        .theme-toggle label::after {
            content: '';
            position: absolute;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background-color: #fff;
            top: 2px;
            left: 2px;
            transition: transform 0.3s, background-color 0.3s;
        }
        .theme-toggle input:checked + label::after {
            transform: translateX(24px);
            background-color: #bb86fc;
        }
        .theme-toggle span {
            margin-right: 10px;
        }
    </style>

    <!-- The most aggressive way to prevent the white flash.
         This script runs immediately and sets the data-theme attribute
         and background color before the body is rendered. -->
    <script>
        (function() {
            const html = document.documentElement;
            const body = document.body;
            const currentTheme = localStorage.getItem('theme');
            if (currentTheme) {
                html.setAttribute('data-theme', currentTheme);
                // Set the background color directly to prevent flicker
                body.style.backgroundColor = currentTheme === 'dark' ? '#121212' : '#f4f4f9';
            }
        })();
    </script>
</head>
<body>
    <div class="theme-toggle">
        <span>Dark Mode</span>
        <input type="checkbox" id="dark-mode-toggle">
        <label for="dark-mode-toggle"></label>
    </div>

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

        const toggleSwitch = document.getElementById('dark-mode-toggle');
        const html = document.documentElement;

        // Set the initial state of the toggle switch on page load
        const currentTheme = localStorage.getItem('theme');
        if (currentTheme === 'dark') {
            toggleSwitch.checked = true;
        }

        toggleSwitch.addEventListener('change', function() {
            if (this.checked) {
                html.setAttribute('data-theme', 'dark');
                localStorage.setItem('theme', 'dark');
            } else {
                html.setAttribute('data-theme', 'light');
                localStorage.setItem('theme', 'light');
            }
        });
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
        return redirect(url_for('home', input_string=input_text, converted_string=converted_text))
    
    input_text = request.args.get('input_string', '')
    converted_text = request.args.get('converted_string', '')

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
        return redirect(url_for('reverse', reverse_input_string=reverse_input_text, reversed_string=reversed_text))
        
    reverse_input_text = request.args.get('reverse_input_string', '')
    reversed_text = request.args.get('reversed_string', '')

    return render_template_string(
        HTML_TEMPLATE,
        reverse_input_text=reverse_input_text,
        reversed_string=reversed_text
    )

if __name__ == '__main__':
    app.run(debug=True)
