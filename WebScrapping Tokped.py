#!/usr/bin/env python
# coding: utf-8

# Scrapping harga GPU RTX 3070 di Tokopedia menggunakan python

# Muhammad Arya Danuarta

# NIM: 09011282025035

'''Proses ini menggunakan file html yang diunduh
Secara langsung dari website target
yang ingin diambil datanya.
Hal ini dilakukan karena response web
pada situs aslinya menggunakan lazy loading 
Sehingga membatasi pengambilan data 
Karena website harus dinavigasi keseluruhan
agar data yang diinginkan termuat.
Menggunakan bantuan beberapa library yang
Bisa dilihat dibawah ini'''

# In[1]:


from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns


# In[2]:


list_item = []
list_harga = []
list_total = []


# In[3]:


with open('Jual rtx 3070 _ Tokopedia.html', 'r') as html_file:
    html = html_file.read()

soup = BeautifulSoup(html, 'lxml')
items = soup.find_all('div', class_='css-12sieg3')


# In[4]:


for item in items:
    nama_item = item.find('div', class_='css-1b6t4dn').text.replace(',', '')
    harga_item = item.find('div', class_='css-1ksb19c').text.replace('Rp', '')

    list_total.append(nama_item)
    list_total.append(harga_item.replace('.', ''))


# In[5]:


f = open('hasil.csv', 'w')
f.write("Nama Barang,Harga\n")

for i in range(len(list_total)):
    if i % 2 == 0:
        f.write((list_total[i] + ','))
        f.write(list_total[i+1])
    else:
        f.write("\n")

f.close()


# In[6]:


df = pd.read_csv('hasil.csv')


# In[7]:


df.head(5)


# In[8]:


df.dtypes


# In[9]:


plt.boxplot(df['Harga'])


# In[10]:


sns.boxplot(x=df['Harga'])


# Kemungkinan besar terdapat outlier yang perlu dieleminasi terlebih dahulu pada dataset, proses dibawah merupakan eliminasi outlier dengan IQR

# In[11]:


Q1 = df.quantile(0.25)
Q3 = df.quantile(0.75)
IQR = Q3 - Q1
print(IQR)


# In[12]:


import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)
compare = [(df < (Q1 - 1.5 * IQR))|(df > (Q3 + 1.5 * IQR))]
print(compare)


# In[13]:


df_out = df[~((df < (Q1 - 1.5 * IQR)) |(df > (Q3 + 1.5 * IQR))).any(axis=1)]
df_out.shape

#opsional jika ingin memuat dataset baru yang sudah dinormalisasi outliernya ke sebuah file
##df.to_csv(hasil_no_outlier, encoding='utf-8', index=False)

# In[14]:


sns.boxplot(x=df_out['Harga'])


# Sekarang dataset lebih tertata tanpa outlier

# In[15]:


sns.displot(df_out['Harga'],kde=True, color='blue', bins=5)


# In[16]:


sns.set(rc={'figure.figsize':(5,5)})
sns.kdeplot(df_out['Harga'],shade=False)


# In[125]:


df_out.mean()


# Rata-rata harga barang terdapat di 1.312107e+07 atau = Rp. 13.121.070

# In[ ]:




