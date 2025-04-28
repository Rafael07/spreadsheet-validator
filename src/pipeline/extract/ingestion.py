import pandas as pd
from ydata_profiling import ProfileReport
import os

data_path = 'data/bronze/'
report_path = 'reports/'

df = pd.read_csv(os.path.join(data_path, 'data.csv'))
profile = ProfileReport(df, title="Pandas Profiling Report")
profile.to_file(output_file=os.path.join(report_path, 'data_report.html'))
