import pandas as pd

df = pd.read_csv('data.csv')

abon_number = 968247916

outgoing = df[df['msisdn_origin'] == abon_number].copy() # Исходящие
incoming = df[df['msisdn_dest'] == abon_number].copy()   # Входящие

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

print('Итоговая сумма: {:.2f}'.format(tariff(outgoing, incoming)))

