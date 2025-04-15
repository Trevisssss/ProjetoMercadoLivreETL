import pandas as pd
import datetime

pd.options.display.max_columns = None
notebook_data = pd.read_json("data\data.json")

notebook_data['created_at'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

print(notebook_data.head())