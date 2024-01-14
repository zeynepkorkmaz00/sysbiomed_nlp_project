from Bio import Entrez
import csv
import os
import xml.etree.ElementTree as ET
import copy

# Function that searches for papers using our SQs and returns a list of PubMed IDs
def search_pubmed_for_ids(query, max_results=13):
    Entrez.email = "zeynep.korkmaz@tum.de"  # Set email address

    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = Entrez.read(handle)
    handle.close()

    return record["IdList"]

# Function that reads the keywords and SQs from a directory with CSV files and returns a dictionary
def read_keywords_from_directory(directory):
    keywords_dict = {}

    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            csv_file = os.path.join(directory, filename)
            
            # for troubleshooting (dictionary only contains 99 files but should contain ~140)
            #print("Reading keywords from file: {}".format(csv_file)) # all files are read

            with open(csv_file, 'r') as file:
                reader = csv.reader(file)

                current_pub_title = None
                current_keywords = []
                current_sq_tp = []
                current_sq_fp = []
                current_sq_r = []

                for row in reader:
                    row = [item.strip(', ') for item in row]
                    if row and not row[0].isdigit():
                        if row[0] == "Pub Title":
                            if current_pub_title:
                                keywords_dict[current_pub_title] = {
                                    "Pub Title": current_pub_title,
                                    "Keywords": current_keywords,
                                    "SQ_TP": current_sq_tp,
                                    "SQ_FP": current_sq_fp,
                                    "SQ_R": current_sq_r
                                }
                            current_pub_title = row[1]
                            current_keywords = []
                            current_sq_tp = []
                            current_sq_fp = []
                            current_sq_r = []
                        elif row[0] == "Keywords":
                            current_keywords.extend(item for item in row[1:] if item)
                        elif row[0] == "SQ_TP":
                            current_sq_tp.extend(item for item in row[1:] if item)
                        elif row[0] == "SQ_FP":
                            current_sq_fp.extend(item for item in row[1:] if item)
                        elif row[0] == "SQ_R":
                            current_sq_r.extend(item for item in row[1:] if item)

                if current_pub_title:
                    keywords_dict[current_pub_title] = {
                        "Pub Title": current_pub_title,
                        "Keywords": current_keywords,
                        "SQ_TP": current_sq_tp,
                        "SQ_FP": current_sq_fp,
                        "SQ_R": current_sq_r
                    }

    return keywords_dict

# Function that takes keyword_dict/input_dict and returns dict with list of PubMed IDs based on SQs
def dict_to_pubmed_id(input_dict):
    # Initialize a new dictionary to store the results
    result_dict = {}

    # Iterate over each publication entry in the input dictionary
    for pub_title, pub_data in input_dict.items():
        # Create a copy of the publication data
        pub_result = pub_data.copy()

        # Initialize empty lists for PubMed IDs for SQ_TP, SQ_FP, and SQ_R
        pub_result['PubMed_IDs_TP'] = []
        pub_result['PubMed_IDs_FP'] = []
        pub_result['PubMed_IDs_R'] = []

        # Extract elements from SQ_TP, SQ_FP, and SQ_R lists and search PubMed for IDs
        for sq_tp_element in pub_data['SQ_TP']:
            pub_result['PubMed_IDs_TP'].extend(search_pubmed_for_ids(sq_tp_element))

        for sq_fp_element in pub_data['SQ_FP']:
            pub_result['PubMed_IDs_FP'].extend(search_pubmed_for_ids(sq_fp_element))

        for sq_r_element in pub_data['SQ_R']:
            pub_result['PubMed_IDs_R'].extend(search_pubmed_for_ids(sq_r_element))

        # Add the modified publication data to the result dictionary
        result_dict[pub_title] = pub_result

    return result_dict

# Function that takes dict with list of PubMeds IDs for the SQs as input, searches specified directory for the corresping XML papers and combines all to one large XML file (output)
import xml.etree.ElementTree as ET

def extract_xml_files(input_dict, input_dir, output_file):
    
    SQ_IDs = {
        'SQ_TP_IDs': [id for pub_title, data in input_dict.items() for id in data['PubMed_IDs_TP']],
        'SQ_FP_IDs': [id for pub_title, data in input_dict.items() for id in data['PubMed_IDs_FP']],
        'SQ_R_IDs': [id for pub_title, data in input_dict.items() for id in data['PubMed_IDs_R']]
    }

    with open(output_file, 'wb') as f:
        f.write(b'<root>\n')

        for SQ, desired_IDs in SQ_IDs.items():
            SQ_root = ET.Element(f'{SQ}')

            for root_dir, dirs, files in os.walk(input_dir):
                for xml_file in files:
                    if xml_file.endswith('.xml'):
                        xml_file_path = os.path.join(root_dir, xml_file)
                        
                        try:
                            tree = ET.parse(xml_file_path)
                        except ET.ParseError:
                            print(f"Skipping file due to ParseError: {xml_file_path}")
                            continue

                        root = tree.getroot()
                        root_copy = copy.deepcopy(root)

                        for element in root_copy.iter('article-id'):
                            if element.attrib.get('pub-id-type') == 'pmid' and element.text in desired_IDs:
                                SQ_root.append(root_copy)

            f.write(ET.tostring(SQ_root, encoding='utf-8'))

        f.write(b'</root>')


## Apply workflow:

# read dir with CSVs and create dict with keywords and SQs
input_dir = "Keyword_CSVs" 
keywords_dict = read_keywords_from_directory(input_dir)

# create dict with PubMed IDs for SQs
pubmed_id_dict = dict_to_pubmed_id(keywords_dict)

# extract XML files for SQs
input_dir = "add directory with XML files here"
output_file = "add output file here"
extract_xml_files(pubmed_id_dict, input_dir, output_file)