import pandas as pd
import numpy as np
import mysql.connector

df = pd.DataFrame(pd.read_excel("students_raw.xlsx"))
df['Name_Clean'] = df['Name'].str.strip().str.lower()
df=df.drop_duplicates(subset=["Name_Clean"],keep="first")
df['Name']=df['Name_Clean']
df=df.drop(columns='Name_Clean')
avggraavg=df.loc[:,"Average Grade"].mean()
df["Average Grade"]=df["Average Grade"].fillna(avggraavg)
# Source - https://stackoverflow.com/a/44133242
# Posted by jezrael, modified by community. See post 'Timeline' for change history
# Retrieved 2026-02-18, License - CC BY-SA 3.0
avgage=int(df.loc[:,"Age"].mean())

dfager = df[(df['Age'] >= 0) | (df['Age'].isnull())]
df["Age"]=dfager["Age"]
df["Age"]=df["Age"].fillna(avgage)
medfood=df.loc[:,"Food Cost"].median()
df["Food Cost"]=df["Food Cost"].fillna(medfood)
df['Total']=df['Rent']+df['Food Cost']
ambition_map = {
    'Low': 1,
    'Medium': 2,
    'High': 3,
    'Extreme': 4
}
print(df.head())

df['Ambition_Score'] = df['Ambition'].map(ambition_map)
cors=df['Ambition_Score'].corr(df['IQ'])
cnx = mysql.connector.connect(
    host="enterhost",
    port="",
    user="enteruser",
    password="enterpassword",
database='enter')
sql = """
    INSERT INTO parser (
        `Student_ID`, `Name`, `Averge_Grade`, `Nationality`, `Age`, 
        `Rent`, `Food_Cost`, `IQ`, `Ambition`, `Total`, `Ambition_Score`
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
cur = cnx.cursor()

for row in df.itertuples(index=False, name=None):
    cur.execute(sql, row)

cnx.commit()
cnx.close()

print ("Done")



