import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import os
from youtube_transcript_api import YouTubeTranscriptApi

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Prompt for generating Gemini content
prompt = """You are Yotube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here: """

# Function to generate Gemini content based on transcript
def generate_gemini_content(transcript_text, prompt):
    try:
        # Model configuration for Gemini
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt + transcript_text)
        return response.text
    except Exception as e:
        return str(e)  # Return the error as text

# Function to extract transcript details from YouTube URL
def extract_transcript_details(url):
    try:
        video_id = url.split("=")[1]
        # Get the transcript text
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)

        # Combine transcript pieces into a single text
        transcript_text = ""
        for i in transcript_list:
            transcript_text += " " + i["text"]

        return transcript_text
    except Exception as e:
        return str(e)  # Return the error as text

# Streamlit UI
st.title("YouTube Transcript Converter")

youtube_link = st.text_input("Enter YouTube Video Link:")

# Display video thumbnail if the link is provided
if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

# Generate detailed notes when the button is clicked
if st.button("Get Detailed Notes"):
    try:
        transcript_text = extract_transcript_details(youtube_link)

        if "Error" in transcript_text:
            st.error(f"Error in extracting transcript: {transcript_text}")
        else:
            summary = generate_gemini_content(transcript_text, prompt)
            st.markdown("## Detailed Notes:")
            st.write(summary)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
