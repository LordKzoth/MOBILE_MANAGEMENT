#!/usr/bin/env python
# coding: utf-8

# # Лабораторная работа №1
# ## Вариант 6
# Протарифицировать абонента с номером <b>968247916</b> с коэффициентом k: 4руб/минута исходящие звонки, 
# 
# 0руб/минута входящие первые 5 минут, далее 1руб/минута, 
# 
# смс - первые 5шт бесплатно, далее 1руб/шт

# In[1]:


import pandas as pd


# In[2]:


df = pd.read_csv('data.csv')
print('Количество строк в таблице: {}'.format(len(df)))


# * timestamp - время звонка
# * msisdn_origin - кто совершил звонок
# * msisdn_dest - кому звонили
# * call_duration - длительность звонка в минутах
# * sms_number - количество отправленных смс для абонента msisdn_origin
# 

# In[4]:


# Перечень абонентов
abon = set()

for v in df['msisdn_origin']:
    abon.add(v)
for v in df['msisdn_dest']:
    abon.add(v)

abon = sorted(list(abon))


# In[5]:


abon_number = 968247916


# ### Исходящие

# In[6]:


outgoing = df[df['msisdn_origin'] == abon_number].copy()


# ### Входящие

# In[9]:


incoming = df[df['msisdn_dest'] == abon_number].copy()


# # Тарификация

# In[11]:


def tariff(outgoing, incoming):
    # Get necessary values from data
    out_calls = outgoing['call_duration'].values
    sms = outgoing['sms_number'].values
    in_calls = incoming['call_duration'].values
    
    # Calculate amount
    out_calls_sum = sum([v * 4 for v in out_calls])
    in_calls_sum  = sum([5*0 + (v-5)*1 if v>=5 else 0 for v in in_calls])
    sms_sum       = sum([5*0 + (v-5)*1 if v>=5 else 0 for v in sms])
    amount =  out_calls_sum + in_calls_sum + sms_sum
    
    return amount


# In[12]:


print('Итоговая сумма: {:.2f}'.format(tariff(outgoing, incoming)))

