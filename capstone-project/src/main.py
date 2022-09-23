import pandas as pd

url = "/Users/renatomeira/project/personal/data-engineering-udacity/capstone-project"


fname = url + "/data/18-83510-I94-Data-2016/i94_apr16_sub.sas7bdat"
df = pd.read_sas(fname, "sas7bdat", encoding="ISO-8859-1")


print(df)
