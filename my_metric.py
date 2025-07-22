from sklearn.metrics import jaccard_score
import pandas as pd
import argparse

def parse_submission(df_submission):
    # print(df_submission.head())
    df_submission["prediction"] = df_submission["prediction"].fillna("")
    predictions_residues = []
    for _, r in df_submission.iterrows():
        for res in r['prediction'].strip().split(" "):
            predictions_residues.append((r['id'], res.strip()))
    df_predictions_residues = pd.DataFrame(predictions_residues, columns=["id", "residue_id"])
    df_predictions_residues["prediction"] = 1
    return df_predictions_residues

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", type=str)
    parser.add_argument("-t", type=str, default=None)
    args = parser.parse_args()

    # read files
    df_submission = pd.read_csv(args.s)
    print("Total PDBs predicted:", df_submission.shape[0])
    df_submission = parse_submission(df_submission)

    df_target = None
    if args.t is not None:
        df_target = pd.read_csv(args.t)
        print("Total PDBs in target:", df_target.shape[0])
        # To make sure parse_submission will work
        if "resid" in df_target.columns:
            df_target.rename(columns={"resid": "prediction"}, inplace=True)
        df_target = parse_submission(df_target)

        # Ensure the columns are named correctly
        df_target.columns = ["id", "residue_id", "true"]
        
    
    df_target_prediction = pd.merge(df_target, df_submission, on=["id", "residue_id"], how="left")
    # print(df_target_prediction.head())
    df_target_prediction["prediction"] = df_target_prediction["prediction"].fillna(0)

    print(df_target_prediction.shape[0], "residue predictions in total")
    y_score = df_target_prediction["prediction"]
    y_true = df_target_prediction["true"]

    print(jaccard_score(y_true, y_score))