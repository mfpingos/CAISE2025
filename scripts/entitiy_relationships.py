import xml.etree.ElementTree as ET
import openai

# Load XML File
xml_file_path = '../data/knowledge/merged.xml'  # Update with your actual file path
tree = ET.parse(xml_file_path)
root = tree.getroot()

# Extract Entities, Keywords, and Data Owners
data = []
for source in root.findall('source'):
    source_name = source.find('stable_attributes/Source_Name').text
    data_owner = source.find('stable_attributes/Data_Owner').text
    keywords = source.find('stable_attributes/Keywords').text.split(', ')
    
    data.append({
        'Source_Name': source_name,
        'Data_Owner': data_owner,
        'Keywords': keywords
    })

# ChatGPT-based Relationship Generator
def generate_relationships_with_chatgpt(data):
    prompt = (
        "You are an intelligent assistant tasked with mapping keywords to meaningful relationships. "
        "Given a data owner and associated keywords, generate relationships in the format: "
        "'Entity A --Relationship--> Entity B', where 'Entity A' is the data owner and 'Entity B' is the keyword. "
        "Use meaningful verbs for the relationships based on the context of the keyword.\n\n"
    )
    for record in data:
        prompt += f"Data Owner: {record['Data_Owner']}\n"
        prompt += f"Keywords: {', '.join(record['Keywords'])}\n\n"

    # Use ChatGPT API to generate relationships
    openai.api_key = ''  # Replace with your OpenAI API key
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    relationships = response['choices'][0]['message']['content']
    return relationships

# Generate relationships
relationships = generate_relationships_with_chatgpt(data)

# Save the relationships or print them
print(relationships)

# Optional: Save relationships to a file
output_file = "../results/entity_relationship/merged_knowledge.txt"
with open(output_file, "w") as file:
    file.write(relationships)

print(f"Relationships saved to {output_file}")
