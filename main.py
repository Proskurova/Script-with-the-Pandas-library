# Скрипт, соединяет 2 базы данных и проверяет наличие одинаковых номеров, в разных форматах и делит на три базы.
# Первая: номера у которых есть ФИО и почта. Вторая: номера у которых есть только почта.
# Третья: номера у которых есть только ФИО.

import pandas as pd

bd1 = pd.read_excel("Database1.xlsx")
df1 = pd.DataFrame(bd1)
bd2 = pd.read_excel("Database2.xlsx")
df2 = pd.DataFrame(bd2)


def reformat(string):
    result = ("+7" + (string.replace('-', '').replace('(', '').replace(')', '').replace(' ', '').replace('+', ''))[-10::1])
    return result


table1_1 = []
table1_2 = []

for value in df1["Номер"]:
    table1_1.append(value)
    table1_2.append(reformat(str(value)))
dict1 = dict(zip(table1_1, table1_2))
df1 = df1.replace({"Номер": dict1})

table2_1 = []
table2_2 = []

for value in df2["Номер"]:
    table2_1.append(value)
    table2_2.append(reformat(str(value)))
dict2 = dict(zip(table2_1, table2_2))
df2 = df2.replace({"Номер": dict2})

one = pd.merge(df1, df2, how='inner', on='Номер')
one.to_excel('One.xlsx', index=True)

two = pd.merge(df2, df1, how='right', on='Номер')
two1 = two[two.isna().any(axis=1)]
two1.to_excel('Two.xlsx', index=True)

three = pd.merge(df1, df2, how='right', on='Номер')
three1 = three[three.isna().any(axis=1)]
three1.to_excel('Three.xlsx', index=True)


