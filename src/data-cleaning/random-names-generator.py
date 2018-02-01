import names

# generate names
NUM_NAMES = 1086

first_names = []
for i in range(NUM_NAMES):
    first_names.append(names.get_first_name())

last_names = []
for i in range(NUM_NAMES):
    last_names.append(names.get_last_name())

# save in excel file
import pandas as pd
import numpy as np

writer = pd.ExcelWriter('random_names.xlsx')
df = pd.DataFrame({"First Name": first_names, "Last Name": last_names})
df.to_excel(writer,'Sheet1', index=False)
# df2.to_excel(writer,'Sheet2')
writer.save()
