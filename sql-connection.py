



import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration
import mysql.connector

# Initialize the tokenizer from Hugging Face Transformers library
tokenizer = T5Tokenizer.from_pretrained('t5-small')

# Load the model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = T5ForConditionalGeneration.from_pretrained('cssupport/t5-small-awesome-text-to-sql')
model = model.to(device)
model.eval()

# Database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'raima',
    'password': '222bda010raima.roj',
    'database': 'airport_practise'
}

def generate_sql(input_prompt):
    # Tokenize the input prompt
    inputs = tokenizer(input_prompt, padding=True, truncation=True, return_tensors="pt").to(device)

    # Forward pass
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=512)

    # Decode the output IDs to a string (SQL query in this case)
    generated_sql = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return generated_sql

def fetch_data_from_database(sql_query):
    try:
        # Connect to the database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Execute the SQL query
        cursor.execute(sql_query)

        # Fetch all the results
        results = cursor.fetchall()

        return results

    finally:
        # Close the database connection
        if connection.is_connected():
            cursor.close()
            connection.close()

# Get user input for the query
enquiry = input() #translation
#input_prompt = "tables:\n" + "CREATE TABLE FL_DETAILS (Flight_Type , Flight_Number, AirlineCode, AirlineName, Scheduled_Time, Estimated_Time, City_Name, City_Code, TerminalName, Gate_Number, Current_Status, Aircraft_Type )" + "\n" +"query for:" + enquiry

arrival_keywords = ['arrive', 'flight','arrival','come','reach','land']
departure_keywords = ['depart', 'flight','take off','fly','go']




if 'when' in enquiry.lower() and any(keyword in enquiry.lower() for keyword in arrival_keywords):

    input_prompt = "tables:\n" + "CREATE TABLE FL_DETAILS (Flight_Type , Flight_Number, AirlineCode, AirlineName, Scheduled_Time, Estimated_Time, City_Name, City_Code, TerminalName, Gate_Number, Current_Status, Aircraft_Type )" + "\n" +"query for: SELECT Estimated_Time FROM FL_DETAILS WHERE Flight_Number = """ +  enquiry
#elif 'delay' in enquiry.lower() 

        
else:
    # Otherwise, use a general prompt
    input_prompt = "tables:\n" + "CREATE TABLE FL_DETAILS (Flight_Type , Flight_Number, AirlineCode, AirlineName, Scheduled_Time, Estimated_Time, City_Name, City_Code, TerminalName, Gate_Number, Current_Status, Aircraft_Type )" + "\n" +"query for:" + enquiry


# Generate SQL query
generated_sql = generate_sql(input_prompt)
print(generated_sql)
# Fetch data from the database using the generated SQL query
result = fetch_data_from_database(generated_sql)

# Display the result
print(result)
