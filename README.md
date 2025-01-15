
# Erl: Your Personal Code Generator

Welcome to **Erl**, your personal AI-powered code generator designed to supercharge your development workflow and help you get your projects off the ground faster. Erl isn't just a tool—it's your partner in innovation, built to seamlessly generate, review, and manage code with precision and speed.

### Preview
![Project Demo](https://cdn.loom.com/sessions/thumbnails/7726e273f081427e99f31539998de834-4459ecb710820bae-full-play.gif)

### Demo
Watch the demo [Click here](https://www.loom.com/share/7726e273f081427e99f31539998de834)

## Features

### 🚀 Supercharge Your Development
Erl helps you:
- Generate high-quality code based on your prompts.
- Create an initial review of the generated code with AI insights.
- Extract files and represent them as JSON for easy integration and manipulation.

### 🛠 Locally Built API
This project includes a locally-hosted API to:
1. **Extract Files as JSON**: Transform files into JSON representations using your custom prompts.
2. **Code Review Endpoint**: Generate detailed AI reviews of your code for best practices, potential improvements, and optimization tips.

### 🔬 Explore AI and Data Manipulation
Erl provides a hands-on experience to:
- Understand how AI language models (LLMs) operate at the data manipulation level.
- Experiment with the integration of AI into real-world development pipelines.

## Getting Started

Follow these steps to get Erl up and running on your local machine:

### 1. Clone the Repository
```bash
git clone <repository_url>
cd erl-code-generator
```

### 2. Prepare to Launch
Set up the necessary permissions for the script:
```bash
chmod 700 run.sh
```
You will need to ensure you have an OPENAI_API_KEY, a GITHUB_TOKEN, and a GITHUB_USER defined as an environment variables.
`export OPENAI_API_KEY="VALUE"`
`export GITHUB_USER="VALUE"`
`export GITHUB_TOKEN="VALUE"`

Important: You will need to buy Open AI credits to run this

### 3. Launch the Process
Run the script to start the API and initialize Erl:
```bash
./run.sh
```

The API will now be live and ready to assist you with code generation and review tasks.
Visit: http://127.0.0.1:5000/apidocs/#/ to see API methods
## How It Works

### File Extraction Endpoint
Submit a file and a prompt to extract meaningful data or transform the file into JSON format. Perfect for structured file manipulation and API integrations.

### Code Review Endpoint
Send your code to this endpoint, and Erl will:
- Analyze it for best practices.
- Suggest improvements and optimizations.
- Identify potential issues and solutions.

## Why Erl?
Erl is more than a project—it's an exploration of how artificial intelligence can transform software development. By examining the relationship between LLMs and data manipulation, Erl offers:
- Insights into the capabilities and limitations of AI in coding tasks.
- A foundation for integrating AI into your development toolkit.

## Contributions
This project is open for collaboration! If you have ideas or enhancements, feel free to open an issue or submit a pull request.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

Get ready to build smarter, faster, and with the power of AI at your fingertips. With Erl, the future of development starts now.
