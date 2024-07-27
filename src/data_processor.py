# data_processor.py
import pandas as pd


class DataProcessingError(Exception):
    """Custom exception for data processing errors."""
    pass


def process_sales_data(data):
    try:
        if not data:
            raise DataProcessingError("Input data is empty")

        df = pd.DataFrame(data)

        required_columns = ['product', 'quantity', 'price']
        if not all(col in df.columns for col in required_columns):
            raise DataProcessingError(f"Input data must contain columns: {required_columns}")

        # Check for non-numeric values in quantity and price
        if not pd.api.types.is_numeric_dtype(df['quantity']) or not pd.api.types.is_numeric_dtype(df['price']):
            raise DataProcessingError("Quantity and price must be numeric")

        # Check for negative values
        if (df['quantity'] < 0).any() or (df['price'] < 0).any():
            raise DataProcessingError("Quantity and price cannot be negative")

        df['total'] = df['quantity'] * df['price']
        grouped = df.groupby('product').agg({
            'total': 'sum',
            'quantity': 'sum'
        }).reset_index()

        # Avoid division by zero
        grouped['average_price'] = grouped.apply(
            lambda row: row['total'] / row['quantity'] if row['quantity'] != 0 else 0,
            axis=1
        )

        return grouped

    except pd.errors.EmptyDataError:
        raise DataProcessingError("Unable to create DataFrame: input data is empty")
    except KeyError as e:
        raise DataProcessingError(f"Missing required column: {str(e)}")
    except TypeError as e:
        raise DataProcessingError(f"Invalid data type: {str(e)}")
    except Exception as e:
        raise DataProcessingError(f"An unexpected error occurred: {str(e)}")


