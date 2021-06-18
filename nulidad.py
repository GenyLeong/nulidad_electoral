# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import numpy as np
import pandas as pd
import datetime as dt
#import seaborn as sns
#import codecs
#import csv
#from zipfile import ZipFile
# from selenium import webdriver
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.support.expected_conditions import presence_of_element_located

import json
import requests


# %%
url = "https://plataformaelectoral.jne.gob.pe/Expediente/BusquedaReporteAvanzadoExpediente"

payload = json.dumps({
    "idProcesoElectoral": 111,
    "idTipoExpediente": 15,
    "idJuradoElectoral": 0,
    "idOrganizacionPolitica": 0,
    "strUbigeo": "000000"
})

headers = {
    'Content-Type': 'application/json',
    'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'
}

response = requests.request("POST", url, headers=headers, data=payload)
# print(response.text)
#data = response.json()
elevations = response.json()
elevations['data']
xls = pd.json_normalize(elevations['data'])
xls


# %%
#browser = webdriver.Chrome(executable_path=r"/usr/local/bin/chromedriver")
#browser = webdriver.Chrome()


# %%
# browser.get('https://plataformaelectoral.jne.gob.pe/Expediente/BusquedaAvanzadaExpediente?')

# WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, "cboProcesoElectoral")))
# select = Select(browser.find_element_by_id('cboProcesoElectoral'))
# browser.implicitly_wait(10)
# select.select_by_value('number:111')

# WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'select[ng-model="t.idTipoExpediente"]')));

# browser.refresh()

# select = Select(browser.find_element_by_css_selector('select[ng-model="t.idTipoExpediente"]'))
# select.select_by_value('number:15')

# browser.find_element_by_class_name('button--is-primary').click()
# browser.implicitly_wait(10)

# browser.find_element_by_css_selector('button[file-name="EXPEDIENTES_SEPEG.2021"]').click()

# list_of_files = glob.glob('/home/geny/Downloads/*.xlsx') # * means all if need specific format then *.csv
# latest_file = max(list_of_files, key=os.path.getctime)

# browser.quit()

# xls = pd.read_excel(latest_file, engine='openpyxl', index_col=0)
# xls


# %%
codigo_csv = pd.read_csv('IDs.csv')
codigo_csv


# %%
id_dict = codigo_csv.to_dict('split')
id_dict['data']


# %%
ids = []
for x in range(len(id_dict['data'])):
    array = id_dict['data'][x][0]
    ids.append(array)

ids


# %%
dptos = []
for x in range(len(id_dict['data'])):
    array = id_dict['data'][x][1]
    dptos.append(array)

dptos


# %%
res = {dptos[i]: ids[i] for i in range(len(ids))}
res


# %%
xls['ID'] = xls['strDepartamento'].map(res)


# %%
for col in xls.columns:
    print(col)


# %%
xls.isnull().sum()


# %%
xls['strTipoEleccion'] = xls['strTipoEleccion'].replace(
    '', 'SEGUNDA VUELTA PRESIDENCIAL')

xls['strEstadoExped'] = xls['strEstadoExped'].replace('', 'SIN INFORMACION')

xls['strOrganizacionPolitica'] = xls['strOrganizacionPolitica'].replace(
    '', 'SIN PARTIDO')
xls['strDepartamento'] = xls['strDepartamento'].replace('', 'SIN DEPARTAMENTO')


# xls = xls.rename(columns={"COD# UBIGEO DOMICILIO": "UBIGEO","PAIS DOMICILIO": "PAIS","DEPARTAMENTO DOMICILIO": "DEPARTAMENTO", "PROVINCIA DOMICILIO": "PROVINCIA", "DISTRITO DOMICILIO": "DISTRITO"})


# %%
xls.head(50)


# %%

find_partido = xls['strOrganizacionPolitica'] == 'FUERZA POPULAR'
#find_materia = xls['strMateria'] == 'APELACIÓN'
#find_estado = xls['strEstadoExped'] == 'RESUELTO'


xls_FP = xls[find_partido]

columnas = ['strOrganizacionPolitica', 'strDepartamento', 'ID',
            'strJuradoElectoral', 'strMateria', 'strEstadoExped']
df_tabla1 = pd.DataFrame(xls_FP, columns=columnas)

df_tabla1 = df_tabla1.rename(columns={"strOrganizacionPolitica": "ORGANIZACIÓN POLÍTICA", "strDepartamento": "DEPARTAMENTO",
                             "strJuradoElectoral": "JURADO ELECTORAL", 'strMateria': 'MATERIA', "strEstadoExped": "ESTADO"})
df_tabla1


# %%
df_tabla1.to_csv('tabla_FP.csv', index=False)


# %%
df_dpto_FP = xls_FP.groupby(
    ['ID', 'strDepartamento', 'strEstadoExped']).size().unstack()
df_dpto_FP = df_dpto_FP.reset_index()
df_dpto_FP = df_dpto_FP.fillna(0)
df_dpto_FP = df_dpto_FP.rename(columns={"strDepartamento": "DEPARTAMENTO"})
#df_dpto_FP['DEPARTAMENTO'] = df_dpto_FP['DEPARTAMENTO'].str.capitalize()

df_dpto_FP


# %%
df_dpto_FP.to_csv('tabla_mapa_FP.csv', index=False)


# %%
regiones_pedidos = xls_FP.groupby(
    ['strDepartamento', 'strOrganizacionPolitica']).size().unstack()
regiones_pedidos = regiones_pedidos.reset_index()
regiones_pedidos = regiones_pedidos.fillna(0)
regiones_pedidos = regiones_pedidos.rename(
    columns={"strDepartamento": "PROCEDENCIA",  "FUERZA POPULAR": "CANTIDAD"})
#df_dpto_FP['DEPARTAMENTO'] = df_dpto_FP['DEPARTAMENTO'].str.capitalize()

regiones_pedidos


# %%
regiones_pedidos.to_csv('pedidos_regiones_FP.csv', index=False)


# %%
find_partido = xls['strOrganizacionPolitica'] == 'FUERZA POPULAR'
#find_materia = xls['strMateria'] == 'REGISTRADO'
find_estado = xls['strEstadoExped'] == 'EN PRONUNCIAMIENTO'


xls_FP = xls[find_partido & find_estado]

columnas = ['strCodExpedienteExt', 'strOrganizacionPolitica', 'strDepartamento',
            'ID',  'strJuradoElectoral', 'strMateria', 'strEstadoExped']
df_tabla_filtro = pd.DataFrame(xls_FP, columns=columnas)

df_tabla_filtro = df_tabla_filtro.rename(columns={"strOrganizacionPolitica": "ORGANIZACIÓN POLÍTICA", "strDepartamento": "DEPARTAMENTO",
                                         "strJuradoElectoral": "JURADO ELECTORAL", 'strMateria': 'MATERIA', "strEstadoExped": "ESTADO"})
df_tabla_filtro


# %%
df_tabla_filtro.to_csv('tabla_apelacion_resuelto_FP.csv', index=False)


# %%
partido = 'PARTIDO POLITICO NACIONAL PERU LIBRE'

xls_PL = xls[xls['strOrganizacionPolitica'] == partido]
xls_PL

columnas = ['strOrganizacionPolitica', 'strDepartamento',
            'ID', 'strJuradoElectoral', 'strMateria', 'strEstadoExped']
df_tabla2 = pd.DataFrame(xls_PL, columns=columnas)
df_tabla2 = df_tabla2.rename(columns={"strOrganizacionPolitica": "ORGANIZACIÓN POLÍTICA", "strDepartamento": "DEPARTAMENTO",
                             "strJuradoElectoral": "JURADO ELECTORAL", 'strMateria': 'MATERIA', "strEstadoExped": "ESTADO"})

df_tabla2


# %%
df_tabla2.to_csv('tabla_PL.csv', index=False)


# %%
df_dpto_PL = xls_PL.groupby(
    ['ID', 'strDepartamento', 'strEstadoExped']).size().unstack()
df_dpto_PL = df_dpto_PL.reset_index()
#df_dpto_PL = df_dpto_PL.fillna(0)
df_dpto_PL = df_dpto_PL.rename(columns={"strDepartamento": "DEPARTAMENTO"})

#df_dpto_PL['DEPARTAMENTO'] = df_dpto_PL['DEPARTAMENTO'].str.capitalize()
df_dpto_PL


# %%
df_dpto_PL.to_csv('tabla_mapa_PL.csv', index=False)


# %%
regiones_pedidos_PL = xls_PL.groupby(
    ['strDepartamento', 'strOrganizacionPolitica']).size().unstack()
regiones_pedidos_PL = regiones_pedidos_PL.reset_index()
regiones_pedidos_PL = regiones_pedidos_PL.fillna(0)
regiones_pedidos_PL = regiones_pedidos_PL.rename(
    columns={"strDepartamento": "PROCEDENCIA",  "PARTIDO POLITICO NACIONAL PERU LIBRE": "CANTIDAD"})
#df_dpto_FP['DEPARTAMENTO'] = df_dpto_FP['DEPARTAMENTO'].str.capitalize()

regiones_pedidos_PL


# %%
regiones_pedidos_PL.to_csv('pedidos_regiones_PL.csv', index=False)


# %%
graficas_csv = pd.read_csv('nulidad_electoral - backup.csv')
graficas_csv


# %%
razones_improcedencia = graficas_csv.groupby(
    ['RAZON', 'DECISION']).size().unstack()
razones_improcedencia = razones_improcedencia.reset_index()
razones_improcedencia = razones_improcedencia.fillna(0)
#razones_improcedencia = razones_improcedencia.rename(columns={"strDepartamento": "PROCEDENCIA",  "PARTIDO POLITICO NACIONAL PERU LIBRE": "CANTIDAD"})
#df_dpto_FP['DEPARTAMENTO'] = df_dpto_FP['DEPARTAMENTO'].str.capitalize()

razones_improcedencia


# %%
razones_improcedencia.to_csv('razones_improcedencia_FP.csv', index=False)
