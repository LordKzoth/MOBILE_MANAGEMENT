# ВАРИАНТ 6
# 
# Протарифицировать абонента с IP-адресом 192.168.250.1 с коэффициентом k: 0,5руб/Мб (ЗАМЕНА: 0,5руб/Кб) первые 500Мб (ЗАМЕНА: 500Кб), 
# после каждых последующих 500Мб (ЗАМЕНА: 500Кб) k увеличивается на 0,5руб

import pandas as pd

# ОБРАБОТКА ФАЙЛА
text = []
with open('nfcapd.txt', 'r', encoding='utf_8') as f:
    text = f.readlines()

spaces = [' '*n for n in range(20, 2, -1)]

for i in range(len(text)):
    text[i] = text[i].replace('->', '')

words = ['INVALID', 'XEvent', 'Ignore']
for word in words:
    for i in range(len(text)):
        text[i] = text[i].replace(word, ' ' + word + ' ')

for space in spaces:
    for i in range(len(text)):
        text[i] = text[i].replace(space, '  ')
            
for i in range(len(text)):
    text[i] = text[i].replace('  ', ',')

        
with open('new_nfcapd.txt', 'w', encoding='utf_8') as f:
    f.writelines(text)


# ПОЛУЧЕНИЕ ЗАПИСЕЙ, КОТОРЫЕ СООТВЕТСТВУЮТ IP, ЗАДАННОМУ ВАРИАНТОМ
df = pd.read_csv('new_nfcapd.txt', sep=',')
df

total_traffic = df[(df['Src IP Addr:Port'].str.contains('192.168.250.1')) | (df['Dst IP Addr:Port'].str.contains('192.168.250.1'))].reset_index(drop=True).copy()
total_traffic['Date first seen'] = total_traffic['Date first seen'].apply(pd.to_datetime).copy()
total_traffic['In Byte'] = total_traffic['In Byte'].apply(lambda x: float(x) if x[-1] != 'M' else float(x[:-1]) * 1024 * 1024).copy()
result = sum(total_traffic['In Byte'].values)
result = round((result / 1024), 2)
print('Итоговый объём трафика: {}Кб'.format(result))


# ОТОБРАЖЕНИЕ ГРАФИКА ЗАВИСИМОСТИ ОБЪЁМА ТРАФИКА ОТ ВРЕМЕНИ
import matplotlib.pyplot as plt

total_traffic['Date first seen'] = total_traffic['Date first seen'].apply(lambda x: str(x)[:str(x).find('.')]).copy()
total_traffic['Date first seen'] = total_traffic['Date first seen'].apply(pd.to_datetime).copy()
total_traffic['Date first seen'] = total_traffic['Date first seen'].apply(lambda x: str(x)[:-3]).copy()
total_traffic['Date first seen'] = total_traffic['Date first seen'].apply(pd.to_datetime).copy()

traffic_after_group = (total_traffic.groupby('Date first seen').aggregate(sum)).copy()
traffic_after_group

plt.figure(figsize=(15, 10))
plt.title('Минуты')
plt.plot(traffic_after_group.index, traffic_after_group['In Byte'].values)

plt.show()


# ТАРИФИКАЦИЯ
total_price = 0
price_per_500 = 0.5

while result > 0:
    total_price += 500 * price_per_500 if result >= 500.0 else result * price_per_500
    
    price_per_500 += 0.5
    result -= 500
    
total_price = round(total_price, 2)

print('Итоговый результат: {}'.format(total_price))