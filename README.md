# Comprehensive Conceptual Model (CCM) Design and Data Mesh Framework

Welcome to the **Comprehensive Conceptual Model (CCM) Design and Data Mesh Framework** repository. 
This project outlines a novel framework for building a CCM using raw data and domain knowledge, creating a Data Mesh, and mapping processes to respective domains to enhance data analysis and decision-making accuracy.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Workflow](#workflow)
- [Key Components](#key-components)
- [Getting Started](#getting-started)
- [References](#license)

---

## Introduction

This repository provides a structured approach to creating a **Comprehensive Conceptual Model (CCM)** using large language models (LLMs) to extract entities and relationships from raw data and domain knowledge. 
The CCM serves as a foundation for designing a **Data Mesh**, enabling domain-specific data management, improved resource allocation, and tailored performance metrics. The running example focuses on healthcare workflows such as **Inpatient** and **Psychiatric procedures** as in [12] [19] in manuscript references, illustrating how to structure data and knowledge for analysis.


---

## Features

### Prerequisites

Ensure you have the following Python libraries installed before running the project:

- **pandas**: For data manipulation and analysis.
- **numpy**: For numerical computations.
- **collections**: Provides specialized container datatypes like `Counter` and `defaultdict`.
- **scikit-learn**:
  - `TfidfVectorizer`: For vectorizing text data.
  - `KMeans`: For clustering.
  - `silhouette_score`: For evaluating clustering performance.
- **os**: To interact with the operating system.
- **re**: For regular expression operations.
- **networkx**: For creating and visualizing graphs.
- **matplotlib**: For plotting and visualizing data.
- **pathlib**: For working with file paths.
- **textwrap**: For formatting text.
- **xml.etree.ElementTree**: For parsing XML data.
- **openai**: For accessing OpenAI APIs (e.g., GPT models).

You can install the required libraries using the following command:

```bash
pip install pandas numpy scikit-learn networkx matplotlib openai

---

## Workflow

The framework follows these steps:

1. Collect **Raw Data** and **Domain Knowledge**.
2. Organize data in a **Data Lake** for accessibility.
3. Construct a **CCM** using LLMs to extract key entities and relationships.
4. Design a **Data Mesh** with identified domains and shared entities.
5. Map processes to appropriate domains for tailored analysis and insights.

For more details, refer to [Fig. 1](#) and the included algorithms in the manuscript.

---

## Key Components

### 1. Raw Data
Collected from various clinical applications such as ticketing systems and bed trackers. Organized into a **Data Lake** for structured processing.

### 2. Domain Knowledge
Contextual insights into attributes such as data owners, data sources, and access control policies.

### 3. CCM Creation
- Entities and relationships extracted using LLMs (e.g., GPT-4).
- Visualized as an **Entity-Relationship Diagram (ERD)** using tools like [Mermaid Charts](https://www.mermaidchart.com/).

### 4. Data Mesh
Data domains identified using clustering techniques, ensuring high-quality data management and domain-specific analysis.

### 5. Process-to-Domain Mapping
Events and relationships analyzed to map processes to appropriate domains for effective resource allocation and performance measurement.

---

## Getting Started

### Prerequisites
- **Python 3.8+**
- Libraries: `numpy`, `pandas`, `sklearn`, `mermaidpy`
- Access to LLM APIs (e.g., OpenAI GPT-4)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/mfpingos/LLM-InterProcessMesh.git

## References

### [12]
Eytan, A., Haller, D.M., Wolff, H., Cerutti, B., Sebo, P., Bertrand, D., Niveau, G.: Psychiatric symptoms, psychological distress and somatic comorbidity among remand prisoners in switzerland. International Journal of Law and Psychiatry 34(1), 13–19 (2011). https://doi.org/https://doi.org/10.1016/j.ijlp.2010.11.003, https://www.sciencedirect.com/science/article/pii/S0160252710001160

### [19]
Mannhardt, F., Koschmider, A., Baracaldo, N., Weidlich, M., Michael, J.: Privacy- Preserving Process Mining. Business & Information Systems Engineering 61(5), 595–614 (Oct 2019). https://doi.org/10.1007/s12599-019-00613-3

