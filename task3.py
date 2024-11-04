import pandas as pd

class Sales:
    def __init__(self, f_path, chunk_size=100000):
        self.f_path = f_path
        self.chunk_size = chunk_size
        self.req_cols = {'product_id', 'price', 'quantity', 'region'}
        self.df = pd.DataFrame()

    def process(self):
        try:
            self._load()
            self._calc_sales()
            self._group_region()
            self._calc_avg_price()
            self._filter()
            self._print_results()
        except FileNotFoundError:
            print(f"Error: File '{self.f_path}' not found.")
        except KeyError as e:
            print(f"Error: {e}")
        except pd.errors.EmptyDataError:
            print("Error: The file is empty.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def _load(self):
        chunk_list = []
        for chunk in pd.read_csv(self.f_path, chunksize=self.chunk_size):
            if not self.req_cols.issubset(chunk.columns):
                raise KeyError(f"Missing columns: {self.req_cols - set(chunk.columns)}")
            chunk = chunk.dropna(subset=['product_id']).drop_duplicates(subset=['product_id'])
            chunk_list.append(chunk)
        self.df = pd.concat(chunk_list, ignore_index=True)

    def _calc_sales(self):
        self.df['sales'] = self.df['price'] * self.df['quantity']

    def _group_region(self):
        self.reg_sales = self.df.groupby('region', as_index=False)['sales'].sum()

    def _calc_avg_price(self):
        avg_price = self.df.groupby('product_id', as_index=False)['price'].mean()
        avg_price.columns = ['product_id', 'avg_price_unit']
        self.df = self.df.merge(avg_price, on='product_id')

    def _filter(self):
        self.filtered = self.df[self.df['sales'] > 10000]

    def _print_results(self):
        print("Total Sales by Region:\n", self.reg_sales)
        print("\nDataset with Average Price per Unit:\n", self.df)
        print("\nFiltered Data (Total Sales > 10,000):\n", self.filtered)

if __name__ == "__main__":
    sales = Sales("sales.csv")
    sales.process()

# Answer to Tricky Aspect of the task
# 1.I read the data in chunks using the chunksize parameter in pd.read_csv(), which allows processing large datasets without overwhelming memory.
# 2.I drop rows with missing or duplicated product_id values early on, which reduces the dataset size and speeds up subsequent operations like grouping and aggregation.
# 3.I ensure data integrity by dropping any rows with NaN values in the product_id column and removing duplicates during the loading process.