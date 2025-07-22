import os
import argparse
import pandas as pd

def main(input_dir, output_file, threshold):
    submission_rows = []

    # Iterate over all files in the directory
    for filename in os.listdir(input_dir):
        if filename.endswith("_predictions.csv"):
            file_path = os.path.join(input_dir, filename)
            df = pd.read_csv(file_path)

            # Extract residue_ids column and split strings into individual residues
            all_residues = []
            for val, prob in zip(df[' residue_ids'].dropna(), df[' probability']):
                if isinstance(val, str) and prob > threshold:
                    all_residues.extend(val.split())

            # Get unique residues and sort them for consistency
            unique_residues = set(all_residues)
            prediction_string = " ".join(unique_residues)

            # Extract ID from filename (before first underscore)
            id_str = filename.split("_")[0]

            # Append to submission data
            submission_rows.append({
                "id": id_str,
                "prediction": prediction_string
            })

    # Create and save the submission DataFrame
    submission_df = pd.DataFrame(submission_rows)
    submission_df["id"] = submission_df["id"].astype(int)
    submission_df = submission_df.sort_values(by="id").reset_index(drop=True)

    print("Files in total:", submission_df.shape[0])
    submission_df.to_csv(output_file, index=False)
    print(f"Submission saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Aggregate P2Rank predictions into a submission file.")
    
    parser.add_argument("-i", "--input", required=True, help="Directory with *_predictions.csv files")
    parser.add_argument("-o", "--output", required=True, help="Output CSV file path (e.g., submission.csv)")
    parser.add_argument("-t", "--threshold", type=float, default=0.0, help="Minimum probability threshold for residue inclusion (default: 0.0)")

    args = parser.parse_args()

    main(args.input, args.output, args.threshold)
