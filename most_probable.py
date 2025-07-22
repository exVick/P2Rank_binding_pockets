import os
import argparse
import pandas as pd

def main(input_dir, output_file):
    """
    Aggregates P2Rank predictions by taking the most probable binding pocket
    from each prediction file and creates a single submission file.
    """
    submission_rows = []

    # Iterate over all files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith("_predictions.csv"):
            file_path = os.path.join(input_dir, filename)
            
            # Read the prediction file
            df = pd.read_csv(file_path)

            # Strip leading/trailing spaces from column names
            df.columns = df.columns.str.strip()

            # Get the prediction from the first row (most probable pocket)
            # If the file is empty or has no 'residue_ids' column, predict an empty string
            if not df.empty and 'residue_ids' in df.columns:
                prediction_string = df.loc[0, 'residue_ids']
            else:
                prediction_string = ""

            # Extract ID from filename (assuming format 'ID_..._predictions.csv')
            id_str = filename.split("_")[0]

            # Append the result to our list
            submission_rows.append({
                "id": id_str,
                "prediction": prediction_string if isinstance(prediction_string, str) else ""
            })


    # Create and save the submission DataFrame
    submission_df = pd.DataFrame(submission_rows)
    submission_df["id"] = submission_df["id"].astype(int)
    submission_df = submission_df.sort_values(by="id").reset_index(drop=True)

    print(f"Files processed in total: {submission_df.shape[0]}")
    submission_df.to_csv(output_file, index=False)
    print(f"Submission saved to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Aggregate P2Rank predictions into a submission file by taking the top prediction."
    )
    
    parser.add_argument(
        "-i", "--input", 
        required=True, 
        help="Directory with input *_predictions.csv files"
    )
    parser.add_argument(
        "-o", "--output", 
        required=True, 
        help="Output CSV file path (e.g., submission.csv)"
    )

    args = parser.parse_args()

    main(args.input, args.output)
