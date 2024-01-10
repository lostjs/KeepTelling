import streamlit as st
import random
import openai

#read openai key from hidden file
def get_api_key():
    with open('openai_key.txt', 'r') as file:
        return file.read()

openai.api_key = get_api_key()

story_elements = [
    "Conflict", "Resolution", "Climax", "Motivation", "Plot Twist",
    "Obstacle", "Foreshadowing", "Protagonist", "Antagonist", 
    "Deuteragonist", "Rival", "Mentor", "Epiphany", "Dialogue", 
    "Flashback", "Setting Description", "Parallel Plot", 
    "Historical Context", "Event", "Suspense"
]

def get_one_random_element(elements):
    return random.choice(elements)

def generate_story_paragraph(messages, element, user_input=None):
    if user_input:
        prompt_content = f'Write a first paragraph of a story about {user_input}. It must include {element}.'
    else:
        prompt_content = f'Write a next paragraph of the given story. It must include {element}.'

    new_message = {
        "role": "user",
        "content": prompt_content
    }

    # Debugging line to display messages
    st.json(messages + [new_message])

    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=0.9,
        messages=messages + [new_message]
    )
    generated_content = response['choices'][0]['message']['content']

    # Not adding history diaglog for new prompt
    messages.extend([new_message, {
         "role": "assistant",
         "content": generated_content
     }])

    return generated_content, messages

# Initialize or use existing messages in session state
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a genius fiction writer. Use the language that's easy to understand even for uneducated people."
        }
    ]

if 'full_story' not in st.session_state:
    st.session_state.full_story = []

def append_to_story(element, paragraph):
    st.session_state.full_story.append({
        "element": element,
        "paragraph": paragraph
    })

def display_full_story():
    for item in st.session_state.full_story:
        st.write(f"Selected Element: {item['element']}")
        st.write(item['paragraph'])

# Streamlit widget for user input on the story's theme or topic
user_input = st.text_input("About what would you like to see a story?")
st.write(f"User input received: {user_input}")  # Debug line to display the user input

if st.button('Generate Story with Random Element'):
    selected_element = get_one_random_element(story_elements)
    story_paragraph, st.session_state.messages = generate_story_paragraph(st.session_state.messages, selected_element, user_input)
    
    # Appending the newly generated paragraph and its associated element to the full story.
    st.session_state.full_story.append({"element": selected_element, "paragraph": story_paragraph})
    
    for section in st.session_state.full_story:
        st.write(f"Selected Element: {section['element']}")
        st.write(section['paragraph'])

if st.button('Continue Story'):
    selected_element = get_one_random_element(story_elements)
    story_paragraph, st.session_state.messages = generate_story_paragraph(st.session_state.messages, selected_element)
    
    st.session_state.full_story.append({"element": selected_element, "paragraph": story_paragraph})
    
    for section in st.session_state.full_story:
        st.write(f"Selected Element: {section['element']}")
        st.write(section['paragraph'])
