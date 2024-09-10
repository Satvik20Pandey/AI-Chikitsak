import pandas as pd
import requests
from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()
SERP_API_KEY = os.getenv('SERP_API_KEY')

def get_disease_info(symptoms):
    query = f"disease information based on symptoms {symptoms}"
    url = f"https://serpapi.com/search.json?api_key={SERP_API_KEY}&q={query}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        results = response.json()
        disease_info = results.get('organic_results', [{}])[0].get('snippet', 'No information found.')
        return disease_info
    except Exception as e:
        return f"Error fetching disease information: {str(e)}"

def get_nearby_hospitals(location):
    query = f"nearby hospitals in {location}"
    url = f"https://serpapi.com/search.json?api_key={SERP_API_KEY}&q={query}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        results = response.json()
        hospitals = [result['name'] for result in results.get('local_results', [])]
        return hospitals
    except Exception as e:
        return [f"Error fetching hospitals: {str(e)}"]

def get_recommended_medicines(symptoms):
    query = f"common medicines for symptoms {symptoms}"
    url = f"https://serpapi.com/search.json?api_key={SERP_API_KEY}&q={query}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        results = response.json()
        medicines = results.get('organic_results', [{}])[0].get('snippet', 'No information found.')
        return medicines
    except Exception as e:
        return f"Error fetching recommended medicines: {str(e)}"

st.title("Disease Detection and Health Info")

st.sidebar.header("Input Symptoms")
symptom_options = ["Fever", "Cough", "Headache", "Nausea", "Fatigue"]
symptoms = {symptom: st.sidebar.checkbox(symptom) for symptom in symptom_options}
custom_symptoms = st.sidebar.text_input("Or enter custom symptoms")

location = st.sidebar.text_input('Enter your location', 'New Delhi')

if st.sidebar.button('Get Information'):
    # Combine selected symptoms and custom symptoms
    selected_symptoms = [symptom for symptom, is_checked in symptoms.items() if is_checked]
    symptoms_str = ', '.join(selected_symptoms + [custom_symptoms]).strip()
    
    if symptoms_str:
        # Fetch disease information
        disease_info = get_disease_info(symptoms_str)
        st.subheader("Disease Information")
        st.write(disease_info)
        
        # Fetch nearby hospitals
        hospitals = get_nearby_hospitals(location)
        st.subheader("Nearby Hospitals")
        if hospitals:
            hospitals_df = pd.DataFrame(hospitals, columns=['Hospital Name'])
            st.dataframe(hospitals_df)
        else:
            st.write("No hospitals found or error occurred.")
        
        # Fetch recommended medicines
        recommended_medicines = get_recommended_medicines(symptoms_str)
        st.subheader("Common Recommended Medicines")
        st.write(recommended_medicines)
    else:
        st.write("Please enter at least one symptom.")
