import os
import shutil
import pandas as pd
import glob


# function that reads SQ pmcids from a csv file and returns a list of pmcids
def read_pmcids_from_csv(input_dir):
    csv_files = glob.glob(os.path.join(input_dir, "PMC*.csv")) # only reads csv files starting with PMC 
    dfs = []

    # Iterate over each CSV file
    for file in csv_files:
        # Read the CSV file into a dataframe
        df = pd.read_csv(file)
        # Append the dataframe to the list
        dfs.append(df)

    # Concatenate all dataframes in the list into a single dataframe (PMC_IDs_TP column contains one long string of PMC_IDs not lists => helper function needed)
    combined_df = pd.concat(dfs)

    # Helper function to extract and clean PMC_IDs from a given column
    def extract_pmcids(column_name):
        pmc_ids_column = combined_df[column_name].tolist()
        pmc_ids = []
        for string in pmc_ids_column:
            if isinstance(string, str):
                list = string.split(',')
                pmc_ids.append(list)
        pmc_ids = [string.replace(" ", "") for sublist in pmc_ids for string in sublist]
        pmc_ids = ['PMC' + string for string in pmc_ids]
        return pmc_ids

    # Use the helper function for each of the columns
    TP_PMC_IDs = extract_pmcids('PMC_IDs_TP')
    FP_PMC_IDs = extract_pmcids('PMC_IDs_FP')
    R_PMC_IDs = extract_pmcids('PMC_IDs_FP')

    return TP_PMC_IDs, FP_PMC_IDs, R_PMC_IDs


def copy_files(input_dir, input_set_pmcids, output_dir):
    # create output dir if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # set of pmcids that have already been found
    previously_found_pmcids = set()

    for subdir, _, files in os.walk(input_dir):  
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(subdir, file)
                file_name = file.split('.')[0]
                # check if file is in input set of pmcids
                if file_name in input_set_pmcids and file_name not in previously_found_pmcids:
                    shutil.copy(file_path, os.path.join(output_dir, file))
                    print(f'Copied {file_name} to {output_dir}')
                    previously_found_pmcids.add(file_name)

def extract_SQ_txt_files(input_dir, input_list_TP_pmcids, input_list_FP_pmcids, input_list_R_pmcids, output_dir_TP, output_dir_FP, output_dir_R):
    copy_files(input_dir, set(input_list_TP_pmcids), output_dir_TP)
    copy_files(input_dir, set(input_list_FP_pmcids), output_dir_FP)
    copy_files(input_dir, set(input_list_R_pmcids), output_dir_R)



# Run script
    
# make lists of PMC IDs from SQ csv files
csv_input_dir = '/nfs/data/pmdb/csv_files'
TP_PMC_IDs, FP_PMC_IDs,R_PMC_IDs = read_pmcids_from_csv(csv_input_dir)

# extract txt files from SQs for PMC10 
input_dir = '/nfs/data/pmdb/pmc_license/other/PMC010xxxxxx'
input_list_TP_pmcids = TP_PMC_IDs
input_list_FP_pmcids = FP_PMC_IDs
input_list_R_pmcids = R_PMC_IDs
output_dir_TP = '/nfs/data/pmdb/SQ_papers/TPs/PMC010xxxxxx_TP_txt_files'
output_dir_FP = '/nfs/data/pmdb/SQ_papers/FPs/PMC010xxxxxx_FP_txt_files'
output_dir_R = '/nfs/data/pmdb/SQ_papers/Rs/PMC010xxxxxx_R_txt_files'
extract_SQ_txt_files(input_dir, input_list_TP_pmcids, input_list_FP_pmcids, input_list_R_pmcids, output_dir_TP, output_dir_FP, output_dir_R)

# extract txt files from SQs for PMC09 
input_dir = '/nfs/data/pmdb/pmc_license/other/PMC009xxxxxx'
input_list_TP_pmcids = TP_PMC_IDs
input_list_FP_pmcids = FP_PMC_IDs
input_list_R_pmcids = R_PMC_IDs
output_dir_TP = '/nfs/data/pmdb/SQ_papers/TPs/PMC009xxxxxx_TP_txt_files'
output_dir_FP = '/nfs/data/pmdb/SQ_papers/FPs/PMC009xxxxxx_FP_txt_files'
output_dir_R = '/nfs/data/pmdb/SQ_papers/Rs/PMC009xxxxxx_R_txt_files'
extract_SQ_txt_files(input_dir, input_list_TP_pmcids, input_list_FP_pmcids, input_list_R_pmcids, output_dir_TP, output_dir_FP, output_dir_R)

# extract txt files from SQs for PMC08 
input_dir = '/nfs/data/pmdb/pmc_license/other/PMC008xxxxxx'
input_list_TP_pmcids = TP_PMC_IDs
input_list_FP_pmcids = FP_PMC_IDs
input_list_R_pmcids = R_PMC_IDs
output_dir_TP = '/nfs/data/pmdb/SQ_papers/TPs/PMC008xxxxxx_TP_txt_files'
output_dir_FP = '/nfs/data/pmdb/SQ_papers/FPs/PMC008xxxxxx_FP_txt_files'
output_dir_R = '/nfs/data/pmdb/SQ_papers/Rs/PMC008xxxxxx_R_txt_files'
extract_SQ_txt_files(input_dir, input_list_TP_pmcids, input_list_FP_pmcids, input_list_R_pmcids, output_dir_TP, output_dir_FP, output_dir_R)

# extract txt files from SQs for PMC07 
input_dir = '/nfs/data/pmdb/pmc_license/other/PMC007xxxxxx'
input_list_TP_pmcids = TP_PMC_IDs
input_list_FP_pmcids = FP_PMC_IDs
input_list_R_pmcids = R_PMC_IDs
output_dir_TP = '/nfs/data/pmdb/SQ_papers/TPs/PMC007xxxxxx_TP_txt_files'
output_dir_FP = '/nfs/data/pmdb/SQ_papers/FPs/PMC007xxxxxx_FP_txt_files'
output_dir_R = '/nfs/data/pmdb/SQ_papers/Rs/PMC007xxxxxx_R_txt_files'
extract_SQ_txt_files(input_dir, input_list_TP_pmcids, input_list_FP_pmcids, input_list_R_pmcids, output_dir_TP, output_dir_FP, output_dir_R)

# extract txt files from SQs for PMC06 
input_dir = '/nfs/data/pmdb/pmc_license/other/PMC006xxxxxx'
input_list_TP_pmcids = TP_PMC_IDs
input_list_FP_pmcids = FP_PMC_IDs
input_list_R_pmcids = R_PMC_IDs
output_dir_TP = '/nfs/data/pmdb/SQ_papers/TPs/PMC006xxxxxx_TP_txt_files'
output_dir_FP = '/nfs/data/pmdb/SQ_papers/FPs/PMC006xxxxxx_FP_txt_files'
output_dir_R = '/nfs/data/pmdb/SQ_papers/Rs/PMC006xxxxxx_R_txt_files'
extract_SQ_txt_files(input_dir, input_list_TP_pmcids, input_list_FP_pmcids, input_list_R_pmcids, output_dir_TP, output_dir_FP, output_dir_R)