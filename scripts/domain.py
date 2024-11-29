import pandas as pd
import numpy as np
from collections import Counter, defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import os
import re

def extract_business_context(entity_a, relationship, entity_b):
    """
    Extract business context from entity-relationship triple.
    Focus on the target entity (Entity B) and its related activities.
    """
    # Process entity B to identify the main business object
    main_object = entity_b.lower()
    words = main_object.split()
    
    # Group related terms and activities
    related_terms = []
    
    # Add relationship context
    related_terms.append(relationship.lower())
    
    # Add entity A context (actor/role)
    related_terms.extend(entity_a.lower().split())
    
    return {
        'main_object': main_object,
        'related_terms': ' '.join(related_terms),
        'full_context': f"{entity_a} {relationship} {entity_b}"
    }

def cluster_by_business_domain(contexts):
    """
    Cluster contexts based on business domain similarity.
    """
    # Create feature vectors focusing on business objects
    vectorizer = TfidfVectorizer(
        stop_words='english',
        ngram_range=(1, 3),  # Allow longer phrases for better context
        max_features=1000
    )
    
    # Combine main objects and related terms with emphasis on the main object
    feature_texts = [
        f"{ctx['main_object']} {ctx['main_object']} {ctx['related_terms']}"
        for ctx in contexts
    ]
    
    vectors = vectorizer.fit_transform(feature_texts)
    
    # Determine optimal number of clusters
    # n_clusters = min(max(3, len(contexts) // 5), 8)  # Adjust range as needed
    n_clusters = min(len(contexts), 5)  # Adjust range as needed
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(vectors)
    
    return cluster_labels

def determine_domain_name(cluster_contexts):
    """
    Determine domain name based on the most significant business objects and their context.
    """
    # Collect all main objects and their frequencies
    main_objects = Counter()
    for ctx in cluster_contexts:
        main_objects.update([ctx['main_object']])
    
    # Get the most common business object
    if not main_objects:
        return "General Domain"
    
    # Find the most representative business object
    common_objects = main_objects.most_common()
    primary_object = common_objects[0][0]
    
    # Clean up the domain name
    domain_name = primary_object.strip()
    
    # Remove generic terms if they appear alone
    generic_terms = {'management', 'system', 'process', 'data'}
    domain_terms = set(domain_name.split())
    if not domain_terms - generic_terms:
        # If only generic terms, use the next most common object
        if len(common_objects) > 1:
            domain_name = common_objects[1][0]
    
    # Construct final domain name
    domain_words = domain_name.split()
    if len(domain_words) > 0:
        # Capitalize each word and ensure "Management" is at the end
        domain_name = ' '.join(word.title() for word in domain_words)
        if 'Management' not in domain_name:
            domain_name += ' Management'
    
    return domain_name

def identify_and_name_data_domains(csv_path):
    """
    Identify and name data domains using business context analysis.
    """
    # Load data
    data = pd.read_csv(csv_path)
    
    # Extract business contexts
    contexts = []
    for _, row in data.iterrows():
        context = extract_business_context(
            row['Entity A'],
            row['Relationship'],
            row['Entity B']
        )
        contexts.append(context)
    
    # Perform clustering
    cluster_labels = cluster_by_business_domain(contexts)
    
    # Generate domain records with context-aware names
    domain_records = []
    for cluster_id in range(max(cluster_labels) + 1):
        # Get contexts for this cluster
        cluster_contexts = [
            ctx for ctx, label in zip(contexts, cluster_labels)
            if label == cluster_id
        ]
        
        # Determine domain name
        domain_name = determine_domain_name(cluster_contexts)
        
        # Add records for this domain
        for i, label in enumerate(cluster_labels):
            if label == cluster_id:
                domain_records.append({
                    "Domain name": domain_name,
                    "Entity A": data.iloc[i]['Entity A'],
                    "Relationship": data.iloc[i]['Relationship'],
                    "Entity B": data.iloc[i]['Entity B']
                })
    
    # Post-process similar domains
    return consolidate_similar_domains(domain_records)

def consolidate_similar_domains(domain_records):
    """
    Consolidate similar domains based on semantic similarity and activity patterns.
    """
    df = pd.DataFrame(domain_records)
    
    # Create vectors for domain comparison
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 3),
        max_features=1000
    )
    
    # For each domain, combine all activities to create a domain profile
    domain_profiles = {}
    for domain in df['Domain name'].unique():
        domain_activities = df[df['Domain name'] == domain]
        profile_text = ' '.join([
            f"{row['Entity A']} {row['Relationship']} {row['Entity B']}"
            for _, row in domain_activities.iterrows()
        ])
        domain_profiles[domain] = profile_text
    
    # Convert profiles to vectors
    profile_texts = list(domain_profiles.values())
    profile_vectors = vectorizer.fit_transform(profile_texts)
    
    # Calculate similarity matrix
    similarity_matrix = (profile_vectors * profile_vectors.T).toarray()
    
    # Group similar domains
    domain_groups = []
    processed_domains = set()
    domains = list(domain_profiles.keys())
    
    for i, domain in enumerate(domains):
        if domain in processed_domains:
            continue
            
        # Find similar domains
        similar_domains = []
        for j, other_domain in enumerate(domains):
            if i != j and other_domain not in processed_domains:
                if similarity_matrix[i, j] > 0.3:  # Adjust threshold as needed
                    similar_domains.append(other_domain)
        
        if similar_domains:
            # Create a group including the current domain
            group = [domain] + similar_domains
            domain_groups.append(group)
            processed_domains.update(group)
        else:
            # Domain stays separate
            domain_groups.append([domain])
            processed_domains.add(domain)
    
    # Create new consolidated domain names based on common elements
    domain_mapping = {}
    for group in domain_groups:
        if len(group) == 1:
            # Single domain remains unchanged
            domain_mapping[group[0]] = group[0]
        else:
            # Analyze activities in the group to determine common focus
            group_activities = df[df['Domain name'].isin(group)]
            
            # Get most common Entity B as it often indicates the domain focus
            common_entity_b = group_activities['Entity B'].mode().iloc[0]
            
            # Clean up the domain name
            domain_name = common_entity_b.strip()
            if 'Management' not in domain_name:
                domain_name += ' Management'
            
            # Map all domains in group to new name
            for domain in group:
                domain_mapping[domain] = domain_name
    
    # Apply mapping
    df['Domain name'] = df['Domain name'].map(domain_mapping)
    
    return df.to_dict('records')

def save_domains_to_csv(domain_records, output_csv_path):
    """
    Save domain records to CSV file.
    """
    domain_df = pd.DataFrame(domain_records)
    domain_df.to_csv(output_csv_path, index=False)
    print(f"Data domains have been saved to {output_csv_path}")

def main():
    csv_path = '../results/entity_relationship/merged_knowledge.csv'
    output_dir = '../results/datamesh'
    os.makedirs(output_dir, exist_ok=True)
    
    domain_records = identify_and_name_data_domains(csv_path)
    output_csv_path = os.path.join(output_dir, 'domains.csv')
    save_domains_to_csv(domain_records, output_csv_path)

if __name__ == "__main__":
    main()