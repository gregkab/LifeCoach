## AI Life Coach

# Project Overview

The AI Life Coach project is an innovative tool designed to assist individuals in tracking their daily thoughts, goals, and reflections. Leveraging FastAPI and the OpenAI API, it integrates advanced AI-driven feedback mechanisms to help users improve productivity and achieve personal goals. This backend service interacts with Notion for data storage and can be complemented by a frontend interface for enhanced user interaction.

# Environment Setup

1. Install Anaconda or Miniconda: Ensure you have Anaconda or Miniconda installed on your machine.

2. Create a Conda Environment: Open your terminal and run the following command to create a new Conda environment named ai-life-coach with Python 3.10.
   bash
   conda create --name ai-life-coach python=3.10

3.Activate the Environment: Activate the newly created environment using:
bash
conda activate ai-life-coach

4. Install Requirements: Navigate to the project directory and install the required packages using:
   bash
   pip install -r requirements.txt

5. Environment Variables: Create a .env file in the root directory and fill in the required API keys and Notion credentials:
   bash
   touch .env

Add the following lines to your .env file:
OPENAI_API_KEY=your_openai_api_key
NOTION_TOKEN=your_notion_integration_token
NOTION_DATABASE_ID=your_notion_database_id

# Running the Application

1. Start the FastAPI Server: Inside the 'api' directory, launch the FastAPI server.

bash
python api/main.py
The server will start on http://localhost:8000.

2. Run the Client Application: In a new terminal window, ensure the ai-life-coach environment is activated and run:

bash
python client/client.py

3. Use the Application: Follow the on-screen prompts in the client application to interact with the AI Life Coach.

# Contributing

This project is in its initial stages and welcomes contributions. Feel free to fork the repository, make your changes, and submit a pull request.

License
All Rights Reserved to Greg Kabakian

Project Structure
AI-Life-Coach/
├── README.md
├── api/
│ ├── **init**.py
│ ├── notion_logic.py
│ └── main.py
├── client/
│ └── client.py
├── requirements.txt
api/: Contains the FastAPI application that handles interactions with Notion and OpenAI's GPT models.
init.py: Makes the api directory a Python package.
notion_logic.py: Contains the API endpoints for fetching logs, adding logs, and generating AI feedback.
main.py: Initializes the FastAPI app and includes the API router.
client/: Contains a simple client application to interact with the API.
client.py: Provides a command-line interface for users to fetch logs, add new logs, and get AI-generated feedback.
requirements.txt: Lists all Python dependencies required to run the project.
README.md: Provides an overview and setup instructions for the project.
Notes
Notion Setup: Ensure that your Notion database has the following properties with exact names: Date, Thoughts, Goals, and Reflections.
OpenAI API Access: Make sure your OpenAI API key has access to GPT-4. If not, you can change the model to gpt-3.5-turbo in notion_logic.py.
Future Enhancements
Frontend Interface: Integrate a web-based frontend using frameworks like Streamlit or React for a more interactive user experience.
Session Management: Implement user authentication and session management for personalized experiences.
Advanced Analytics: Add features to provide analytics and insights over time based on the user's logs.
Acknowledgements
Special thanks to the contributors and the open-source community for providing valuable resources and inspiration.
Enjoy your journey towards improved productivity and goal achievement with your AI Life Coach!
