# AI Headshot Generator

A web application that transforms casual photos into professional business headshots for LinkedIn using AI.

## Features

- Upload casual photos through a user-friendly interface
- AI-powered transformation to professional headshots
- Side-by-side comparison of original and transformed images
- Easy download of the generated headshot

## Prerequisites

- Python 3.7+
- Replicate API key (for AI image processing)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/ai-headshot-generator.git
   cd ai-headshot-generator
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with your Replicate API key:
   ```
   REPLICATE_API_TOKEN=your_replicate_api_key_here
   ```
   You can get an API key by signing up at [replicate.com](https://replicate.com)

## Usage

1. Start the Flask development server:
   ```
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000
   ```

3. Upload a casual photo and get your professional headshot!

## How It Works

The application uses the Replicate API to access a fine-tuned AI model that specializes in transforming casual photos into professional headshots. The process involves:

1. User uploads a photo through the web interface
2. The photo is sent to the Replicate API
3. The AI model processes the image, enhancing it to look like a professional headshot
4. The result is displayed alongside the original for comparison

## Customization

You can modify the app.py file to customize various aspects of the application:

- Change the AI model used for processing
- Adjust image processing parameters
- Customize the upload and result directories

## License

MIT 