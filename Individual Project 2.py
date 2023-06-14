
#Import libraries
import pandas as pd
from plotly.subplots import make_subplots
import seaborn as sns
import streamlit as st
import plotly.express as px
#load the dataset
df = pd.read_csv("ahmad/heart_2020_cleaned.csv")
print(df.head())
# Rename columns to include spaces
df = df.rename(columns={
    "HeartDisease": "Heart Disease",
    "AlcoholDrinking": "Alcoholic",
    "PhysicalHealth": "Physical Health",
    "MentalHealth": "Mental Health Score",
    "DiffWalking": "Difficulty Walking",
    "AgeCategory": "Age",
    "PhysicalActivity":"Physical Activity" ,
    "GenHealth": "General Health",
    "SleepTime": "Sleep Time",
    "KidneyDisease": "Kidney Disease",
    "SkinCancer": "Skin Cancer"
})
# Exploratory Data Analysis
df.info()
# Check for null values
df.isna().sum()

# Check number of patients having heart disease
df["Heart Disease"].value_counts()

# Check for duplicates
df.duplicated().sum()

# Remove the duplicates
df.drop_duplicates(inplace=True)

# Filter the dataset to include only individuals with heart disease
df = df[df['Heart Disease'] == 'Yes']
df.head()
def main():
    quote = "“The problem with heart disease is that the first symptom is often fatal.” — Michael Phelps"
    st.markdown(f"> {quote}")
# Create a Streamlit app and set the title


st.title("Heart Disease: A Modern Health Challenge")
markdown_text = """
Heart disease is on the rise due to modern factors. Sedentary lifestyles, unhealthy diets, stress, smoking, and excessive alcohol consumption contribute to this trend. To combat heart disease, prioritize physical activity, healthy eating, stress management, and avoiding harmful habits. Let's work together for better heart health.
"""

st.markdown(markdown_text)
# Add title for the left side
st.sidebar.title("Configure the Plots")
# Add trendy news about CVD
col1, col2, col3 = st.columns(3)
col1.metric("Smoking", "Chance of CVD", "30%")
col2.metric("Good Physical Health", "Chance of CVD", "-48%")
col3.metric("Good Mental Health", "Chance of CVD", "-13%")


# Add a selectbox to the sidebar to allow the user to choose a variable
variable = st.sidebar.selectbox("Select a variable", df.columns)

# Add range filter on the left sidebar
if df[variable].dtype == 'object':
    unique_values = df[variable].unique()
    selected_values = st.sidebar.multiselect("Select Values", unique_values, default=unique_values)
    filtered_data = df[df[variable].isin(selected_values)]
else:
    range_min = st.sidebar.slider("Range Min", min_value=df[variable].min(), max_value=df[variable].max(), value=(df[variable].min(), df[variable].max()), step=0.01)
    range_max = st.sidebar.slider("Range Max", min_value=df[variable].min(), max_value=df[variable].max(), value=(df[variable].min(), df[variable].max()), step=0.01)
    filtered_data = df[(df[variable] >= range_min[0]) & (df[variable] <= range_max[0])]

# Display the difference in heart disease rates based on the selected variable using visualizations
if variable != 'Heart Disease':
    # Calculate count for each category
    count = filtered_data[variable].value_counts().reset_index()
    count.columns = ['Category', 'Count']
    
    # Plot the count using a vertical bar chart
    st.subheader(f"Vertical Bar Chart: {variable} Count")
    fig_bar_vertical = px.bar(count, x='Category', y='Count', labels={'Category': variable, 'Count': 'Count'})
    st.plotly_chart(fig_bar_vertical)

    # Plot the count using a pie chart
    st.subheader(f"Pie Chart: {variable} Distribution")
    fig_pie = px.pie(count, values='Count', names='Category', labels={'Category': variable, 'Count': 'Count'})
    st.plotly_chart(fig_pie)

    # Plot the count using a treemap
    st.subheader(f"Treemap: {variable} Distribution")
    fig_treemap = px.treemap(count, path=['Category'], values='Count', labels={'Category': variable, 'Count': 'Count'})
    st.plotly_chart(fig_treemap)


# Generate correlation matrix
correlation_matrix = df.corr()

# Create subplots
fig = make_subplots(rows=2, cols=2, subplot_titles=("Plot 1", "Plot 2", "Plot 3", "Plot 4"))


# Plot the correlation matrix heatmap
sns.heatmap(correlation_matrix, annot=True, cbar=False, cmap='RdBu', ax=ax)

# Add a title to the heatmap
st.title("Correlation Matrix for the Numerical Variables")

# Adjust the size of the heatmap on the Streamlit page
st.pyplot(fig)
def prevention_section():
    st.title("Prevention Measures")
    st.write("Preventing heart disease is crucial for maintaining a healthy lifestyle. Heart disease is a leading cause of death worldwide, and it is often preventable through simple lifestyle modifications. Regular exercise, proper nutrition, avoiding smoking, managing stress, and getting regular medical check-ups are some of the key preventive measures. By taking proactive steps to prevent heart disease, we can significantly reduce the risk and improve overall heart health.")

    # Define the prevention measures with statements
    prevention_measures = {
        'Exercise regularly': 'Regular exercise helps maintain a healthy heart.',
        'Do medical check-ups frequently': 'Regular medical check-ups allow early detection and prevention of heart disease.',
        'Give up smoking': 'Smoking significantly increases the risk of heart disease.',
        'Keep diabetes under control': 'Proper diabetes management reduces the risk of heart disease.',
        'Eat a healthy balanced diet': 'A nutritious diet promotes heart health.'
    }

    # Define the wrong answers with statements
    wrong_answers = {
        'Eat cholesterol and fat-rich food a lot': 'Consuming excessive cholesterol and fat-rich food can contribute to heart disease.',
        'Experience stress and depression a lot': 'Chronic stress and depression can negatively impact heart health.',
        'Smoke regularly': 'Smoking is a major risk factor for heart disease.',
        'Drink alcohol on a regular basis': 'Regular alcohol consumption can increase the risk of heart disease.',
        'Be physically inactive': 'Physical inactivity is associated with a higher risk of heart disease.'
    }

    # Combine the correct answers and wrong answers for the options
    options = list(prevention_measures.keys()) + list(wrong_answers.keys())

    # Display the question and answer options
    st.markdown("How can we prevent heart disease?")
    selected_measure = st.selectbox("Select a prevention measure:", options)

    # Check if the selected answer is correct or wrong
    if selected_measure in prevention_measures:
        st.write("Correct!")
    elif selected_measure in wrong_answers:
        st.write("Wrong! " + wrong_answers[selected_measure])

    # Display the selected prevention measure statement
    if selected_measure in prevention_measures:
        st.write(prevention_measures[selected_measure])
# Display content for the 'Prevention' section
prevention_section()
if __name__ == '__main__':
    main()
