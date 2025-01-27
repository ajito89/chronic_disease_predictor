from together import Together
import streamlit as st
import os

def get_llm_recommendation(condition_data):
    """Generate recommendations using Llama model based on condition data"""
    try:
        # Debug print
        print("\nDebug - Attempting to generate recommendations")
        print(f"Input data: {condition_data}")
        
        # Get API key from Streamlit secrets
        api_key = st.secrets['api_keys']['togetherapi']
        print(f"API key found: {'Yes' if api_key else 'No'}")
        
        if not api_key:
            raise ValueError("API key not found")
        
        # Set API key as an environment variable
        os.environ['TOGETHER_API_KEY'] = api_key
        print("API key set in environment variable")
        
        # Create Together client
        client = Together()
        print("Together client created successfully")
        
        # Construct prompt
        prompt = f"""Given a patient with (maximum 250 words):
Primary condition: {condition_data['primary_condition']} (confidence: {condition_data['confidence']*100:.1f}%)
Risk level: {condition_data['risk_level']}
Additional conditions to consider:
{condition_data['condition_list']}

Please provide specific recommendations for:
1. Lifestyle modifications
2. Health monitoring requirements
3. When to seek medical attention
4. Preventive measures"""

        print(f"\nDebug - Sending prompt to API:\n{prompt}")
        
        # Make API call
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.2-3B-Instruct-Turbo",
            messages=[{
                "role": "system", 
                "content": "You are a medical AI assistant providing evidence-based health recommendations."
            }, {
                "role": "user", 
                "content": prompt
            }],
            temperature=0.7,
            max_tokens=500
        )
        
        print("\nDebug - API response received")
        print(f"Response type: {type(response)}")
        print(f"Response content: {response}")
        
        if hasattr(response, 'choices') and len(response.choices) > 0:
            recommendations = response.choices[0].message.content
            print(f"\nDebug - Generated recommendations:\n{recommendations}")
            return recommendations
            
    except Exception as e:
        print(f"\nDebug - Error occurred: {str(e)}")
        print(f"Error type: {type(e)}")
        st.error(f"Error generating recommendations: {str(e)}")
    
    print("\nDebug - Falling back to default recommendations")
    return "Unable to generate recommendations at this time. Please try again later."


def format_recommendations(llm_output):
    """Format the LLM output into structured recommendations"""
    try:
        # Split recommendations into sections
        sections = llm_output.split('\n')
        formatted_recommendations = []
        
        for section in sections:
            if section.strip():
                # Remove numbering and clean up
                cleaned_section = section.strip().lstrip('123456789.)-• ')
                if cleaned_section:
                    formatted_recommendations.append(f"- {cleaned_section}")
        
        return '\n'.join(formatted_recommendations)
    except Exception as e:
        print(f"Error in formatting recommendations: {str(e)}")
        return llm_output


# Example usage
if __name__ == "__main__":
    # Example input data
    condition_data = {
        "primary_condition": "Liver Disease (Hepatitis Cirrhosis) Post Transplant",
        "confidence": 0.95,
        "risk_level": "High",
        "condition_list": "Diabetes, Hypertension, Anemia"
    }
    
    # Get recommendations
    recommendations = get_llm_recommendation(condition_data)
    
    if recommendations:
        formatted_recommendations = format_recommendations(recommendations)
        print("\nFormatted Recommendations:")
        print(formatted_recommendations)
