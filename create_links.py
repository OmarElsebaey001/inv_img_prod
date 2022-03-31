import urllib.parse
import pandas as pd 

data_file = "data.csv"
website = "https://invimgs.herokuapp.com/?"

df = pd.read_csv(data_file)
df = df.replace(r'\t','', regex=True)
df = df.replace(r',','', regex=True)
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
links =[]
for i in range(len(df)):
    params = {
        'cl_nm' : df['Client Name'][i],
        'cl_nt_cp' : int(float(df['Net Capital Invested'][i])),
        'cl_tot_po' : int(float(df['Total Portfolio Value'][i])),
        'wlt_mng': df['Name of Wealth Manager'][i],
        'wlt_mng_nm' : df['Number of Wealth Manager'][i]
    }
    link = website+urllib.parse.urlencode(params,'/', safe='')
    links.append(link)
df['link'] = links
df.to_csv("out.csv",index=False)