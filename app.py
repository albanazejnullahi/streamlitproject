import streamlit as st
import pandas as pd
import re

def main():
    st.title('Excel Data Selector')

    file_path = 'data_streamlit.xlsx'
    try:
        df = pd.read_excel(file_path, engine='openpyxl')
    except Exception as e:
        st.error(f"Error loading Excel file: {e}")
        return
    
    # Ensure all columns are stripped of leading/trailing spaces
    df.columns = df.columns.str.strip()
    
    # Convert all relevant columns to string type
    df['Model'] = df['Model'].astype(str)
    df['Property Name'] = df['Property Name'].astype(str)
    df['Subject Data'] = df['Subject Data'].astype(str)
    df['Comp Data'] = df['Comp Data'].astype(str)
    df['Narrative'] = df['Narrative'].astype(str)
    
    unique_values_column1 = df['Model'].unique().tolist() if 'Model' in df.columns else []
    unique_values_column2 = df['Property Name'].unique().tolist() if 'Property Name' in df.columns else []
    
    unique_values_column1.insert(0, 'Select Model')
    unique_values_column2.insert(0, 'Select Property Name')

    with st.sidebar:
        st.subheader('Filters')
        selected_column1_value = st.selectbox("Select Model", unique_values_column1, key='model_dropdown', help="Select the Model")
        selected_column2_value = st.selectbox("Select Property Name", unique_values_column2, key='property_dropdown', help="Select the Property Name")

    if selected_column1_value != 'Select Model' and selected_column2_value != 'Select Property Name':
        if selected_column1_value == 'Select Model':
            filtered_df = df[df['Property Name'] == selected_column2_value]
        elif selected_column2_value == 'Select Property Name':
            filtered_df = df[df['Model'] == selected_column1_value]
        else:
            filtered_df = df[(df['Model'] == selected_column1_value) & 
                             (df['Property Name'] == selected_column2_value)]

        st.header("Filtered Data")

        if filtered_df.empty:
            st.warning("No data found with the selected criteria.")
        else:
            for index, row in filtered_df.iterrows():
                st.markdown(f"### Model: {row['Model']} | Property Name: {row['Property Name']}")
                
                st.markdown("---")

                # Display Subject Data and Comp Data side by side
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"### Subject Data")
                    formatted_subject_data = format_text(row['Subject Data'], add_space=False)
                    st.markdown(formatted_subject_data, unsafe_allow_html=True)

                with col2:
                    st.markdown(f"### Comp Data")
                    formatted_comp_data = format_text(row['Comp Data'], add_space=False)
                    st.markdown(formatted_comp_data, unsafe_allow_html=True)

                st.markdown("---")

                # Display Narrative
                st.markdown(f"### Narrative")
                formatted_narrative = format_text(row['Narrative'], add_space=True)
                st.markdown(formatted_narrative, unsafe_allow_html=True)

                st.markdown("---")

    else:
        st.info("Please select both Model and Property Name to see filtered data.")

def format_text(text, add_space):
    text = re.sub(r'(^o )', r'* ', text, flags=re.MULTILINE)

    if add_space:
        # Add white space between paragraphs
        formatted_text = text.replace("\n", "<br><br>")
    else:
        formatted_text = text.replace("\n", "<br>")
    
    formatted_text = re.sub(r'\b(\w+italic\w+)\b', r'<i>\1</i>', formatted_text, flags=re.IGNORECASE)
    
    formatted_text = formatted_text.replace("$", "\$")
    
    return formatted_text

if __name__ == "__main__":
    main()
