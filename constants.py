# extract_data, FileHandler
FILE_NAME = 'Result Table.Result'
CSV_FILE_NAME = '_New_Results.csv'
AGGREGATED_CSV_FILE_NAME = '_Aggregated_New_Results.csv'
DATA_FILE_NAME = 'Result Table.Result'
MODE_GENERAL = 'general'
MODE_SELECTIVE = 'selective'
INFO_TYPES_LIST = ['emission', 'dpi']
MODE_TYPES_LIST = ['general', 'selective']
IMPORTANT_COL_NAMES = ['Frequency', 'Data Set', 'Limit Line']

# DataHandler
DATA_HEADER = 'TableValues'
TYPE_EMISSION = 'emission'
TYPE_DPI = 'dpi'
COLUMN_NAME_HEADER = 'Name='

# Column Indices for info types
EMISSION_COL_INDEXES = [0, 1] # 0: Frequency, 1: PK+_CLRWR
DPI_COL_INDEXES = [0, 1]    # 0: Frequency, 1: Imm Lvl-Pk

# File naming
KEYS = []

# Identifier columns for info types
EMISSION_IDENTIFIERS = ['Part ID', 'PG', 'Trim', 'Choke']
DPI_IDENTIFIERS = ['Part ID', 'PG', 'Package', '-', '-', '-', 'Choke', 'Test1Col', 'Test2Col', 'Test3Col', 'Test4Col', '-', '-', '-', '-', 'Test5Col']

# Limit Line
LL_FREQUENCY_LIST = []
IGNORE_LL_HEADER = 'TargetLevel.LimitLine'
LIMIT_LINE_FILE_SUFFIX = '.LimitLine'