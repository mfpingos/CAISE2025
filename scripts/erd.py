import os

def read_relationships_from_file(file_path):
    """Read relationships from file with detailed logging."""
    print(f"\n=== Reading File ===")
    print(f"Attempting to read from: {os.path.abspath(file_path)}")
    
    try:
        if not os.path.exists(file_path):
            print(f"ERROR: File not found: {file_path}")
            return None
        
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            print(f"\nFile contents ({len(content.split('\n'))} lines):")
            print("First 5 lines:")
            for line in content.split('\n')[:5]:
                print(f"  {line}")
            return content
            
    except Exception as e:
        print(f"ERROR reading file: {str(e)}")
        return None

def sanitize_node_text(text):
    """Sanitize node text by removing or replacing special characters."""
    original = text
    # Remove leading '>' and any surrounding whitespace
    text = text.strip().lstrip('>')
    # Replace any remaining special characters with spaces
    result = text.strip()
    if original != result:
        print(f"Sanitized: '{original}' -> '{result}'")
    return result

def create_node_id(text):
    """Create a valid Mermaid node ID from text."""
    # First sanitize the text
    text = sanitize_node_text(text)
    # Replace spaces and special characters with underscores
    return text.replace(' ', '_').replace('-', '_')

def create_mermaid_code(content):
    """Convert content to Mermaid diagram code with proper formatting and logging."""
    print("\n=== Creating Mermaid Code ===")
    
    # Initialize Mermaid diagram
    mermaid_lines = [
        "graph TD",
        "    %% Styles",
        "    classDef default fill:#f9f9f9,stroke:#333,stroke-width:2px;",
        ""
    ]
    
    # Use sets to store unique nodes and relationships
    nodes = set()
    # Use a set of tuples for relationships to ensure uniqueness
    unique_relationships = set()
    
    print("\nParsing relationships:")
    # First pass: collect all unique nodes and relationships
    for line in content.split('\n'):
        line = line.strip()
        if '--' in line and '-->' in line:
            try:
                source = line.split('--')[0].strip()
                target = line.split('-->')[1].strip()
                relationship = line.split('--')[1].split('-->')[0].strip()
                
                # Only print if this is a new relationship
                relationship_tuple = (source, relationship, target)
                if relationship_tuple not in unique_relationships:
                    print(f"  Found new: {source} --{relationship}--> {target}")
                    nodes.add(source)
                    nodes.add(target)
                    unique_relationships.add(relationship_tuple)
                else:
                    print(f"  Skipping duplicate: {source} --{relationship}--> {target}")
            except Exception as e:
                print(f"  ERROR parsing line: '{line}' - {str(e)}")
    
    print(f"\nUnique nodes found ({len(nodes)}):")
    for node in sorted(nodes):
        print(f"  - {node}")
    
    print(f"\nUnique relationships found ({len(unique_relationships)}):")
    for rel in sorted(unique_relationships):
        print(f"  - {rel[0]} --{rel[1]}--> {rel[2]}")
    
    # Add node definitions
    print("\nGenerating node definitions:")
    for node in sorted(nodes):
        sanitized_text = sanitize_node_text(node)
        node_id = create_node_id(node)
        node_def = f"    {node_id}[\"{sanitized_text}\"]"
        print(f"  {node_def}")
        mermaid_lines.append(node_def)
    
    # Add empty line for readability
    mermaid_lines.append("")
    
    # Second pass: add unique relationships
    print("\nGenerating relationships:")
    for source, relationship, target in sorted(unique_relationships):
        try:
            source_id = create_node_id(source)
            target_id = create_node_id(target)
            relationship_line = f"    {source_id} -->|{relationship}| {target_id}"
            print(f"  {relationship_line}")
            mermaid_lines.append(relationship_line)
        except Exception as e:
            print(f"  ERROR creating relationship: {source} -> {target} - {str(e)}")
    
    return "\n".join(mermaid_lines)

def save_mermaid_file(mermaid_code, output_file):
    """Save the Mermaid code to a file with verification."""
    print("\n=== Saving Output ===")
    print(f"Saving to: {os.path.abspath(output_file)}.mmd")
    
    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(f"{output_file}.mmd", "w", encoding="utf-8") as f:
            f.write(mermaid_code)
        
        # Verify the file was written
        if os.path.exists(f"{output_file}.mmd"):
            print("File successfully saved!")
            file_size = os.path.getsize(f"{output_file}.mmd")
            print(f"File size: {file_size} bytes")
        else:
            print("ERROR: File was not created!")
            
    except Exception as e:
        print(f"ERROR saving files: {str(e)}")

def main():
    print("=== ERD Generator Debug Mode (with Deduplication) ===")
    
    # File paths
    input_path = "../results/entity_relationship/"
    input_file = "merged_knowledge.csv"
    
    # Resolve and verify paths
    input_file_name = os.path.splitext(input_file)[0]
    in_file = f"{input_path}{input_file_name}.txt"
    output_file = f"../results/erd/{input_file_name}.txt"
    
    print("\nPaths:")
    print(f"Working directory: {os.getcwd()}")
    print(f"Input path: {os.path.abspath(input_path)}")
    print(f"Input file: {os.path.abspath(in_file)}")
    print(f"Output file: {os.path.abspath(output_file)}")
    
    # Check if directories exist
    print("\nDirectory check:")
    print(f"Input directory exists: {os.path.exists(input_path)}")
    print(f"Input file exists: {os.path.exists(in_file)}")
    print(f"Output directory exists: {os.path.exists(os.path.dirname(output_file))}")
    
    # Read content from file
    content = read_relationships_from_file(in_file)
    if not content:
        return
    
    # Create Mermaid code
    mermaid_code = create_mermaid_code(content)
    
    # Save the file
    save_mermaid_file(mermaid_code, output_file)
    
    print("\nProcess complete!")

if __name__ == "__main__":
    main()