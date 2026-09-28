import pandas as pd


def load_csv(file_path):
    """
    Load a CSV file into a pandas DataFrame.
    """

    try:
        df = pd.read_csv(file_path)
        return df

    # PAY ATTENTION:
    # We catch specific errors instead of catching every possible Exception.
    except FileNotFoundError:
        print(f"Error: file not found -> {file_path}")
        return None

    except pd.errors.EmptyDataError:
        print("Error: the CSV file is empty.")
        return None

    except pd.errors.ParserError:
        print("Error: the CSV file could not be parsed.")
        return None


def inspect_dataframe(df):
    """
    Display basic information about the DataFrame.
    """

    # PAY ATTENTION:
    # df.shape returns TWO values:
    # (number_of_rows, number_of_columns)
    #
    # We can unpack them into separate variables.
    rows, columns = df.shape

    print("\n--- DATAFRAME OVERVIEW ---")

    print(f"Rows: {rows}")
    print(f"Columns: {columns}")

    print("\nColumn Names:")
    print(df.columns.tolist())

    print("\nData Types:")
    print(df.dtypes)

    print("\nDataFrame Info:")

    # PAY ATTENTION:
    # df.info() already prints its own output.
    # So we do NOT write print(df.info()).
    df.info()

    print("\nFirst 5 Rows:")
    print(df.head())


def check_data_quality(df):
    """
    Check missing values and duplicate rows.
    """

    print("\n--- DATA QUALITY ---")

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDuplicate Rows:")
    print(df.duplicated().sum())


def produce_statistics(df):
    """
    Produce basic statistics and identify numerical/categorical columns.
    """

    print("\n--- STATISTICS ---")

    # PAY ATTENTION:
    # select_dtypes() returns a DataFrame containing columns
    # matching the datatype we specify.
    #
    # .columns gets the column names.
    # .tolist() converts those names into a normal Python list.
    numerical_columns = (
        df.select_dtypes(include="number")
        .columns
        .tolist()
    )

    categorical_columns = (
        df.select_dtypes(exclude="number")
        .columns
        .tolist()
    )

    print("\nNumerical Columns:")
    print(numerical_columns)

    print("\nCategorical Columns:")
    print(categorical_columns)

    print("\nNumerical Statistics:")

    # PAY ATTENTION:
    # describe() gives statistics such as:
    # mean, std, min, max, quartiles, etc.
    print(df.describe())


def main():
    """
    Control the overall flow of the program.
    """

    # PAY ATTENTION:
    # Replace this filename with the actual name of YOUR CSV.
    file_path = "data/nigeria_phishing_dataset.csv"

    # Step 1: Load the CSV.
    df = load_csv(file_path)

    # PAY ATTENTION:
    # If load_csv() failed, it returned None.
    #
    # In that situation, we stop here instead of passing
    # None into all the other functions.
    if df is None:
        return

    # Step 2: Run the rest of our program.
    inspect_dataframe(df)
    check_data_quality(df)
    produce_statistics(df)


# PAY ATTENTION:
# This tells Python:
#
# "Only run main() when this file itself is executed."
#
# We'll discuss this in more depth later.
if __name__ == "__main__":
    main() 