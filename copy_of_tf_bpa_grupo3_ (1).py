# -*- coding: utf-8 -*-
"""Copy of TF_BPA_Grupo3 .ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/17tpF0Cj0Pg9h70Dkgn0n-4uNwgit3lAy

# Colectar los datos

## Cargamos Drive

## Carga de las librerías
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy as scipy
import seaborn as sns
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeRegressor, plot_tree
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.metrics import make_scorer, mean_absolute_error
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.metrics import classification_report
from sklearn.metrics import roc_curve, roc_auc_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import RandomizedSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectFromModel
from sklearn.metrics import roc_auc_score,confusion_matrix,f1_score,classification_report,\
                            accuracy_score,precision_score,recall_score

from xgboost import XGBClassifier
from sklearn.model_selection import GridSearchCV

#Desactivar la notación científica
pd.options.display.float_format = '{:.3f}'.format

pd.options.display.max_columns = None

"""## Carga de datos"""

df_cancer = pd.read_csv("/content/lung_cancer_data.csv", encoding='ISO-8859-1')

"""Ahora mostramos el dataset"""

df_cancer.head(5)

"""Acá se logra ver que nuestro dataset tiene 23658 filas y 38 columnas"""

df_cancer.shape

"""Acá se logra ver todas las columnas con su tipo de dato"""

df_cancer.info();

"""# Calidad y limpieza de datos

Primero vamos a ver y analizar si existen valores que se repitan
"""

df_cancer[df_cancer.duplicated()]

"""Como se logra observar no hay valores duplicados

Ahora vamos a ver si existen valores nulos o vacios
"""

(df_cancer.isnull().sum(axis=1)/df_cancer.shape[1]*100).sort_values(ascending=False)

"""Como se logra observar, no existen valores nulos o vacios en nuestro dataset

Ahora vamos a renombrar las columnas que creemos necesarias

Acá consideramos que la única columna a renombrar será "Tumor_Size_mm" por "Tumor_Size_In_Milimeters
"""

columnas_renombrar = {'Tumor_Size_mm':'Tumor_Size_In_Milimeters'}
df_cancer.rename(columns = columnas_renombrar, inplace = True)

"""Ahora vamos a eliminar las columnas que no aportan nada en nuestro modelo predictivo sobre el cáncer de pulmon"""

print(df_cancer.columns)

"""Acá identificamos que las siguientes columnas no nos sirven para nuestro análisis
*  Patient_ID
*  Alanine_Aminotransferase_Level
*  Aspartate_Aminotransferase_Level
*  Creatinine_Level
*  LDH_Level
*  Calcium_Level
*  Phosphorus_Level
*  Glucose_Level
*  Potassium_Level
*  Sodium_Level
"""

df_cancer.drop(columns=['Patient_ID','Creatinine_Level','LDH_Level','Calcium_Level','Phosphorus_Level','Glucose_Level',
                        'Potassium_Level','Sodium_Level','Alanine_Aminotransferase_Level','Aspartate_Aminotransferase_Level','Performance_Status','Alkaline_Phosphatase_Level'], inplace=True)

df_cancer.shape

df_cancer.head(5)

"""Ahora vamos a ver los outliners de nuestras columnas

Primero las categóricas
"""

df_cat = df_cancer.select_dtypes(exclude='number').copy()
df_cat.head(5)

df_cat.info();

"""Acá analizamos cada columna para ver si existen outliner, pero vemos que no hay"""

#df_cat['Gender'].value_counts()*100/len(df_cat)
#df_cat['Smoking_History'].value_counts()*100/len(df_cat)
#df_cat['Tumor_Location'].value_counts()*100/len(df_cat)
#df_cat['Stage'].value_counts()*100/len(df_cat)
#df_cat['Treatment'].value_counts()*100/len(df_cat)
#df_cat['Insurance_Type'].value_counts()*100/len(df_cat)
#df_cat['Family_History'].value_counts()*100/len(df_cat)
#df_cat['Comorbidity_Diabetes'].value_counts()*100/len(df_cat)
#df_cat['Comorbidity_Hypertension'].value_counts()*100/len(df_cat)
#df_cat['Comorbidity_Chronic_Lung_Disease'].value_counts()*100/len(df_cat)
#df_cat['Comorbidity_Kidney_Disease'].value_counts()*100/len(df_cat)
#df_cat['Comorbidity_Autoimmune_Disease'].value_counts()*100/len(df_cat)
df_cat['Comorbidity_Other'].value_counts()*100/len(df_cat)

"""Ahora vamos a analizar las numéricas"""

df_num = df_cancer.select_dtypes(include='number').copy()
df_num.head(5)

df_num.info()

df_num.describe().T

df_num.boxplot()

# Exportar el DataFrame al formato pickle
df_cancer.to_excel('dataset_limpiocancer.xlsx')

# Confirmar exportación
print("Dataset exportado como 'dataset_limpiocancer.xlsx'")

"""# EDA

Ahora, vamos a  realizar el EDA que básicamente es el análisis exploratorio de datos para examinar los datos obtenidos para poder plantear preguntas y sean respondidas
"""

plt.figure(figsize=(8, 8))
df_cancer['Stage'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=['lightblue', 'lightgreen', 'lightcoral', 'orange'])
plt.title('Proporción de Pacientes por Etapa del Cáncer')
plt.ylabel('')
plt.show()

"""Conclusiones:
- Se observa una distribución relativamente uniforme entre las etapas del cáncer de pulmón (Stage I, II, III, IV), lo que sugiere que el dataset abarca pacientes en todas las etapas de la enfermedad, siendo ligeramente mayor la proporción de pacientes en Stage IV (25.4%).
- La mayor frecuencia en Stage IV puede indicar una tendencia en los diagnósticos realizados en etapas avanzadas, probablemente debido a la detección tardía del cáncer, lo que es un reflejo común en la epidemiología de esta enfermedad.
- La presencia de un porcentaje significativo de pacientes en Stage I y II (cerca del 50% en conjunto) destaca la importancia de diseñar estrategias de intervención temprana, que podrían mejorar significativamente las tasas de supervivencia.






"""

plt.figure(figsize=(10, 6))
sns.countplot(data=df_cancer, x='Stage', hue='Treatment', palette='pastel')
plt.title('Distribución de tratamientos por Stage', fontsize=16)
plt.xlabel('Stage', fontsize=12)
plt.ylabel('Cantidad de pacientes', fontsize=12)
plt.legend(title='Treatment', fontsize=10)
plt.show()

"""Conclusiones:


- Se observa que los cuatro tipos de tratamiento principales (Surgery, Radiation Therapy, Chemotherapy y Targeted Therapy) tienen una distribución similar en cada etapa del cáncer, lo que indica que no existe una preferencia marcada de un tratamiento específico para una etapa particular.
- La similitud en las cantidades para cada tratamiento dentro de cada etapa podría reflejar el uso frecuente de tratamientos combinados, donde múltiples enfoques terapéuticos son aplicados simultáneamente para maximizar los resultados clínicos.
- Tanto en Stage I como en Stage IV se presentan cantidades similares de pacientes tratados, lo que sugiere que tanto en etapas iniciales como avanzadas los médicos optan por estrategias de tratamiento diversificadas, aunque las intenciones terapéuticas puedan variar (curativas en etapas tempranas y paliativas en avanzadas).



"""

plt.figure(figsize=(10, 6))
sns.countplot(data=df_cancer, x='Stage', hue='Smoking_History', palette='husl')
plt.title('Distribución de Smoking History por Stage', fontsize=16)
plt.xlabel('Stage', fontsize=12)
plt.ylabel('Cantidad de pacientes', fontsize=12)
plt.legend(title='Smoking History', fontsize=10)
plt.show()

"""Conclusiones

- En todas las etapas del cáncer, se observa una distribución relativamente equilibrada entre fumadores actuales (Current Smoker) y exfumadores (Former Smoker). Esto sugiere que, independientemente de la etapa del cáncer, el historial de tabaquismo juega un papel importante en el diagnóstico de los pacientes.
- En comparación con las otras categorías, los pacientes que nunca fumaron constituyen la menor proporción en todas las etapas del cáncer. Esto refuerza la asociación del tabaquismo con el desarrollo del cáncer de pulmón, como lo han señalado múltiples estudios médicos.
- Las proporciones de las categorías de historial de tabaquismo son consistentes a lo largo de las diferentes etapas (Stage I a IV). Esto indica que el historial de tabaquismo es un factor presente en todas las etapas del cáncer, no mostrando una correlación evidente con una etapa específica.


"""

comorbidities = ['Comorbidity_Diabetes', 'Comorbidity_Hypertension', 'Comorbidity_Heart_Disease']
df_cancer[comorbidities + ['Stage']].melt(id_vars='Stage').pipe(
    lambda df: sns.countplot(data=df, x='Stage', hue='value', palette='viridis')
)

"""Conclusiones

- En todas las etapas del cáncer (Stage I a IV), se observa una distribución consistente entre los pacientes que presentan comorbilidades como diabetes, hipertensión y enfermedades cardíacas, y aquellos que no las tienen. Esto indica que la prevalencia de estas comorbilidades no parece variar significativamente según la etapa del cáncer.
- Un número considerable de pacientes diagnosticados con cáncer de pulmón presenta al menos una comorbilidad (valor "Yes"). Esto refuerza la importancia de considerar estas condiciones como factores críticos al momento de planificar tratamientos y predicciones.
- Aunque el gráfico no muestra diferencias drásticas por etapa, las comorbilidades como hipertensión y enfermedades cardíacas son factores conocidos que podrían complicar el manejo clínico del cáncer de pulmón. Esto subraya la necesidad de incorporar estas variables en los modelos predictivos para capturar su impacto en la progresión de la enfermedad.






"""

sns.countplot(data=df_cancer, x='Ethnicity', hue='Stage', palette='cool')

"""Conclusiones

- En vista generales, podemos observar que las etnias “Caucasian” y “African Americans” tienen más población en todo el dataset. En relación a las Etapas del cáncer, la Etapa IV y III están entre las dos más comúnes en todo las etnias. De igual manera, el Stage II tiene una representación más baja en general.
- Como la Etapa I es de las menos comunes en todas las etnias, podemos concluir que  existen disparidades en el diagnóstico temprano o el acceso a la atención médica entre los grupos étnicos.




"""

plt.figure(figsize=(15, 12))


plt.subplot(2, 2, 3)
sns.boxplot(data=df_cancer, x='Comorbidity_Diabetes', y='Platelet_Count', hue='Stage', palette='muted')
plt.title('Platelet Count vs Diabetes Comorbidity (según Etapa)', fontsize=14)
plt.xlabel('Diabetes Comorbidity', fontsize=12)
plt.ylabel('Platelet Count (x10^3/µL)', fontsize=12)


plt.subplot(2, 2, 4)
sns.boxplot(data=df_cancer, x='Comorbidity_Hypertension', y='Albumin_Level', hue='Stage', palette='viridis')
plt.title('Albumin Level vs Hypertension Comorbidity (según Etapa)', fontsize=14)
plt.xlabel('Hypertension Comorbidity', fontsize=12)
plt.ylabel('Albumin Level (g/dL)', fontsize=12)

plt.tight_layout()
plt.show()

"""Conclusiones:


<u>Conteo de plaquetas vs. Comorbilidad de diabetes (según etapa):</u>
- Con respecto a la distribución general, los pacientes con y sin comorbilidad de diabetes presentan una amplia variabilidad en el conteo de plaquetas. Además, la mediana del conteo de plaquetas parece ser similar entre los pacientes con y sin diabetes.
- En cuanto a la diferenciación por etapas, en etapas avanzadas (e.g., "Stage III" y "Stage IV"), el rango del conteo de plaquetas parece más amplio, con valores extremos más altos. Por otro lado, las etapas iniciales presentan una distribución más concentrada.

<u>Nivel de albúmina vs. Comorbilidad de hipertensión (según etapa):</u>
- En cuanto la diferenciación por etapas, En "Stage IV", los niveles de albúmina tienden a ser más bajos, especialmente en pacientes con hipertensión.Por otro lado, en etapas iniciales ("Stage I" y "Stage II"), los niveles de albúmina son más altos y menos dispersos, indicando un mejor estado nutricional o metabólico.
- En conclusión, la hipertensión parece tener un impacto negativo en los niveles de albúmina, lo que podría relacionarse con un peor pronóstico en pacientes con cáncer en etapas avanzadas





"""

stages = df_cancer['Stage'].unique()

plt.figure(figsize=(25, 9))

# Crear un gráfico para cada etapa
for i, stage in enumerate(stages):
    # Filtrar los datos para cada etapa
    df_stage = df_cancer[df_cancer['Stage'] == stage]

    # Subgráfico para la etapa i (en una fila con tantas columnas como etapas)
    plt.subplot(1, len(stages), i + 1)
    sns.kdeplot(data=df_stage, x='Smoking_Pack_Years', y='Hemoglobin_Level', cmap='Blues', fill=True, alpha=0.6)
    plt.title(f'Smoking Pack Years vs Hemoglobin Level (Stage {stage})', fontsize=14)
    plt.xlabel('Smoking Pack Years', fontsize=12)
    plt.ylabel('Hemoglobin Level', fontsize=12)


plt.tight_layout()
plt.show()

"""Conclusiones

- A nivel general en todos los gráficos, En las cuatro etapas del cáncer, se observa una concentración similar de densidad en torno a valores intermedios de Smoking Pack Years (10 a 50 años) y niveles de Hemoglobin entre 12 y 16 g/dL. Sin embargo, existe una menor densidad en los extremos, como pacientes con más de 80 años de tabaquismo o niveles de hemoglobina más bajos (<\10 g/dL).

- En cuanto al análisis por etapas, parece tener una distribución uniforme, con pocos valores extremos tanto en Smoking Pack Years como en Hemoglobin Level. En cuanto a la Etapa II se encuentra similar a la etapa previa, aunque se aprecia una mayor densidad de pacientes con niveles de hemoglobina más bajos (10-12 g/dL). Por otro lado, en las etapas avanzadas (II y IV), la densidad se concentra más hacia niveles bajos de hemoglobina, lo que puede ser indicativo de un mayor impacto del cáncer en el estado general de salud y nutrición del paciente.

- Aunque los valores de años de tabaquismo son consistentes a través de las etapas, los niveles de hemoglobina tienden a reducirse en las etapas avanzadas. Esto podría sugerir que, aunque el tabaquismo es un factor de riesgo común, el avance del cáncer tiene un impacto más significativo en los niveles de hemoglobina.





"""

stages = df_cancer['Stage'].unique()
plt.figure(figsize=(15, 10))

for i, stage in enumerate(stages, 1):
    plt.subplot(2, 2, i)
    sns.kdeplot(
        data=df_cancer[df_cancer['Stage'] == stage],
        x='Hemoglobin_Level',
        y='White_Blood_Cell_Count',
        fill=True,
        cmap='coolwarm',
        alpha=0.6
    )
    plt.title(f'Hemoglobin vs WBC Count (Stage {stage})', fontsize=14)
    plt.xlabel('Hemoglobin Level', fontsize=12)
    plt.ylabel('White Blood Cell Count (x10^3/µL)', fontsize=12)

plt.tight_layout()
plt.show()

"""Conclusiones:

- Los valores se concentran principalmente entre 12 y 16 g/dL, lo que parece ser el rango típico de los pacientes en todas las etapas. Los valores extremos (por debajo de 10 g/dL o por encima de 18 g/dL) son menos frecuentes.
- Se observa una mayor densidad en el rango de 4 a 8 (x10³/µL), que coincide con los valores normales de referencia en una población sana. Hay algunos pacientes con valores elevados (>10 x10³/µL), lo cual podría estar relacionado con infecciones, inflamación o efectos del cáncer.
- Los niveles de hemoglobina tienden a disminuir ligeramente con el avance de las etapas, mientras que el conteo de glóbulos blancos muestra mayor variabilidad en las etapas avanzadas (III y IV). En Stage III y IV, los valores fuera del rango normal son más frecuentes, reflejando el impacto sistémico de la progresión del cáncer. Por último, la relación entre estas dos métricas podría ser útil para identificar estados inflamatorios o infecciosos en pacientes con cáncer de pulmón.




"""

df_cancer.shape

"""# Transformación de los datos

Separar las variables dependientes e independientes
"""

X = df_cancer.drop(columns='Stage')
y = df_cancer['Stage']

"""Dividir en conjunto de Train y Test"""

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

"""##**Transformacion de Categoricas**

Vamos a transformar primero las variables categóricas de nuestro dataset

*   Gender : (Male, Female)
*   Smoking_History : (Current Smoker, Never smoked, Former Smoker)
*   Tumor_Location: (Lower Lobe, Middle Lobe , Upper Lobe)
*   Treatment: (Chemotherapy, Radiation Therapy, Surgery, Targeted Therapy)
*   Ethnicity: (African American, Asian, Caucasian, Hispanic, Other)
*   Insurance_Type: (Medicare, Medicaid, Private, Other)
*   Family_History: (Yes,No)
*   Comorbidity_Diabetes: (Yes,No)
*   Comorbidity_Hypertension: (Yes,No)
*   Comorbidity_Heart_Disease: (Yes,No)
*   Comorbidity_Chronic_Lung_Disease: (Yes,No)
*   Comorbidity_Kidney_Disease: (Yes,No)
*   Comorbidity_Autoimmune_Disease: (Yes,No)
*   Comorbidity_Other: (Yes,No)
"""

df_cancer.select_dtypes(exclude='number')

"""Ordenamos por variables categóricas nominales y ordinales.

**Nominales:**
*   Gender : (Male, Female)
*   Smoking_History : (Current Smoker, Never smoked, Former Smoker)
*   Tumor_Location: (Lower Lobe, Middle Lobe , Upper Lobe)
*   Treatment: (Chemotherapy, Radiation Therapy, Surgery, Targeted Therapy)
*   Ethnicity: (African American, Asian, Caucasian, Hispanic, Other)
*   Insurance_Type: (Medicare, Medicaid, Private, Other)
*   Family_History: (Yes,No)
*   Comorbidity_Diabetes: (Yes,No)
*   Comorbidity_Hypertension: (Yes,No)
*   Comorbidity_Heart_Disease: (Yes,No)
*   Comorbidity_Chronic_Lung_Disease: (Yes,No)
*   Comorbidity_Kidney_Disease: (Yes,No)
*   Comorbidity_Autoimmune_Disease: (Yes,No)
*   Comorbidity_Other: (Yes,No)

---

Finalmente, clasificamos las variables en one hot encoder, label encoder y ordinal encoder y quedaría de la siguiente forma.

**Label Encoder:**
*   Family_History: (Yes,No)
*   Comorbidity_Diabetes: (Yes,No)
*   Comorbidity_Hypertension: (Yes,No)
*   Comorbidity_Heart_Disease: (Yes,No)
*   Comorbidity_Chronic_Lung_Disease: (Yes,No)
*   Comorbidity_Kidney_Disease: (Yes,No)
*   Comorbidity_Autoimmune_Disease: (Yes,No)
*   Comorbidity_Other: (Yes,No)


**One Hot Encoder**
*   Gender : (Male, Female)
*   Smoking_History : (Current Smoker, Never smoked, Former Smoker)
*   Tumor_Location: (Lower Lobe, Middle Lobe , Upper Lobe)
*   Treatment: (Chemotherapy, Radiation Therapy, Surgery, Targeted Therapy)
*   Ethnicity: (African American, Asian, Caucasian, Hispanic, Other)
*   Insurance_Type: (Medicare, Medicaid, Private, Other)

### Label Encoder
"""

from sklearn.preprocessing import LabelEncoder

columnas = ['Family_History','Comorbidity_Diabetes','Comorbidity_Hypertension','Comorbidity_Heart_Disease','Comorbidity_Chronic_Lung_Disease','Comorbidity_Kidney_Disease',
            'Comorbidity_Autoimmune_Disease','Comorbidity_Other']

#Crear dataframe
X_train_lab_encoded = pd.DataFrame(index=X_train.index)  # Iniciar con el índice original
X_test_lab_encoded = pd.DataFrame(index=X_test.index)    # Iniciar con el índice original

# Inicializar LabelEncoder
label_encoders = {}
for col in columnas:
    labENC = LabelEncoder()
    # Ajustar y transformar el conjunto de entrenamiento
    X_train_lab_encoded[col] = labENC.fit_transform(X_train[col])

    # Solo transformar el conjunto de prueba
    X_test_lab_encoded[col] = labENC.transform(X_test[col])

    label_encoders[col] = labENC  # Guardar el codificador para futuras transformaciones

X_test_lab_encoded

"""Logramos convertir nuestras variables que habíamos definido anteriormente para el método de label encoder. Las variables ahora son unos y ceros

Tenemos:

*   Family_History: (Yes: 1,No: 0)
*   Comorbidity_Diabetes: (Yes: 1,No: 0)
*   Comorbidity_Hypertension: (Yes: 1,No: 0)
*   Comorbidity_Heart_Disease: (Yes: 1,No: 0)
*   Comorbidity_Chronic_Lung_Disease: (Yes: 1,No: 0)
*   Comorbidity_Kidney_Disease: (Yes: 1,No: 0)
*   Comorbidity_Autoimmune_Disease: (Yes: 1,No: 0)
*   Comorbidity_Other: (Yes: 1,No: 0)

### One Hot Encoder
"""

from sklearn.preprocessing import OneHotEncoder

columnas = ['Gender','Smoking_History','Tumor_Location','Treatment','Ethnicity','Insurance_Type']
oneHE = OneHotEncoder(sparse_output = False, dtype='int64', handle_unknown='ignore')

# Fit the encoder on the training data
oneHE.fit_transform(X_train[columnas])

#Apply the encoded for train
X_train_ohe_encoded = pd.DataFrame(oneHE.transform(X_train[columnas]),
                               columns=oneHE.get_feature_names_out(columnas),
                               index=X_train.index)

#Apply the encoded for test
X_test_ohe_encoded = pd.DataFrame(oneHE.transform(X_test[columnas]),
                              columns=oneHE.get_feature_names_out(columnas),
                              index=X_test.index)

X_train_ohe_encoded

"""##Transformación de Numéricas"""

df_cancer.select_dtypes(include='number')

"""###MinMaxScaler"""

from sklearn.preprocessing import MinMaxScaler

# Definir las columnas numéricas que deseas escalar
columnas = ['Age', 'Tumor_Size_In_Milimeters', 'Blood_Pressure_Systolic',
            'Blood_Pressure_Diastolic', 'Blood_Pressure_Pulse', 'Hemoglobin_Level',
            'White_Blood_Cell_Count', 'Platelet_Count', 'Albumin_Level', 'Smoking_Pack_Years', 'Survival_Months']

# Inicializar el MinMaxScaler
encoderMMS = MinMaxScaler()

# Ajustar el scaler al conjunto de entrenamiento
encoderMMS.fit(X_train[columnas])

# Aplicar la transformación en el conjunto de entrenamiento
X_train_mms_encoded = pd.DataFrame(encoderMMS.transform(X_train[columnas]),
                                   columns=columnas,
                                   index=X_train.index)

# Aplicar la transformación en el conjunto de prueba
X_test_mms_encoded = pd.DataFrame(encoderMMS.transform(X_test[columnas]),
                                  columns=columnas,
                                  index=X_test.index)

X_test_mms_encoded

"""##Transformación de la Target"""

y_test

# Transformar y_train en binario (Stage I, II -> 0; Stage III, IV -> 1)
y_train_binario = y_train.replace({'Stage I': 0, 'Stage II': 0, 'Stage III': 1, 'Stage IV': 1})

# Transformar y_test en binario
y_test_binario = y_test.replace({'Stage I': 0, 'Stage II': 0, 'Stage III': 1, 'Stage IV': 1})

y_train_binario

"""---

##Integración de los DataFrames
"""

# Reiniciar índices para evitar problemas de alineación
X_train_lab_encoded.reset_index(drop=True, inplace=True)
X_test_lab_encoded.reset_index(drop=True, inplace=True)
X_train_ohe_encoded.reset_index(drop=True, inplace=True)
X_test_ohe_encoded.reset_index(drop=True, inplace=True)
X_train_mms_encoded.reset_index(drop=True, inplace=True)
X_test_mms_encoded.reset_index(drop=True, inplace=True)
y_train_binario.reset_index(drop=True, inplace=True)
y_test_binario.reset_index(drop=True, inplace=True)

# Concatenar todas las transformaciones en los conjuntos de entrenamiento
X_train_encoded = pd.concat([X_train_lab_encoded, X_train_ohe_encoded, X_train_mms_encoded], axis=1)
X_test_encoded = pd.concat([X_test_lab_encoded, X_test_ohe_encoded, X_test_mms_encoded], axis=1)

# Añadir la target binaria a los conjuntos de entrenamiento y prueba
df_train = pd.concat([X_train_encoded, y_train_binario], axis=1)
df_test = pd.concat([X_test_encoded, y_test_binario], axis=1)

# Combinar ambos conjuntos en un solo DataFrame completo
df_tcancer = pd.concat([df_train, df_test], axis=0).reset_index(drop=True)

df_tcancer

# Número de filas del dataset original
print(f"Número de filas en el dataset original: {df_cancer.shape[0]}")  # Cambia 'df_original' por el nombre original

# Número de filas después de las transformaciones
print(f"Número de filas en el dataset transformado: {df_tcancer.shape[0]}")

# Exportar el DataFrame al formato pickle
df_tcancer.to_pickle('dataset_completotransformado.pkl')

# Confirmar exportación
print("Dataset exportado como 'dataset_completotransformado.pkl'")

"""# Modelización

## Regresión logística
"""

#df_tcancer = pd.read_pickle('dataset_completotransformado.pkl')

X = df_tcancer.drop(columns='Stage')
y = df_tcancer['Stage']

modelo_Reglogistica = LogisticRegression(class_weight='balanced', solver='liblinear')

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) #usamos el 20% de los datoos para el entrenamiento del modelo

modelo_Reglogistica.fit(X_train,y_train)

y_pred_RLog       = modelo_Reglogistica.predict(X_test)
y_pred_RLog_proba = modelo_Reglogistica.predict_proba(X_test)

confusion_matrix_RLog = confusion_matrix(y_test,y_pred_RLog)

# Crear DataFrame de la matriz de confusión con etiquetas claras
confusion_matrix_df = pd.DataFrame(
    confusion_matrix_RLog,
    columns=['Predicción No Grave', 'Predicción Grave'],
    index=['Real No Grave', 'Real Grave']
)

# Mostrar la matriz de confusión
print(confusion_matrix_df)

#Mostrar el confusion matrix como grafico

# Crear DataFrame de la matriz de confusión con etiquetas descriptivas
confusion_matrix_df = pd.DataFrame(
    confusion_matrix_RLog,
    columns=['Predicción No Grave', 'Predicción Grave'],
    index=['Real No Grave', 'Real Grave']
)

# Mostrar la matriz de confusión con un gráfico de heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(
    confusion_matrix_df,
    annot=True,
    fmt='d',
    cmap='Blues',
    annot_kws={"size": 14},
    cbar=False,  # Eliminar la barra de color si no es necesaria
    linewidths=0.5  # Agregar bordes para claridad
)
plt.title("Matriz de Confusión - Clasificación Binaria", fontsize=16)
plt.xlabel("Predicción", fontsize=14)
plt.ylabel("Real", fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12, rotation=0)
plt.show()

from sklearn.metrics import classification_report

# Reporte de clasificación
print("Reporte de clasificación:")
print(classification_report(y_test, y_pred_RLog, target_names=['No Grave', 'Grave']))

"""## Random Forest"""

#df_tcancer = pd.read_pickle('dataset_completotransformado.pkl')

# Separar características y target
X = df_tcancer.drop(columns='Stage',axis=1)
y = df_tcancer['Stage']

# Dividir el dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

modelo_RandomForest = RandomForestClassifier(random_state=42)

modelo_RandomForest.fit(X_train, y_train)
y_pred_train = random_forest.predict(X_train)
# Calcular métricas
print('Train \n',classification_report(y_train, y_pred_train))

# Predecir con el conjunto de prueba
y_pred      = modelo_RandomForest.predict(X_test)
y_pred_prob = modelo_RandomForest.predict_proba(X_test)[:,1]

# Calcular métricas
print('Test \n',classification_report(y_test, y_pred))

print('Test AUC: ',roc_auc_score(y_test, y_pred_prob))

confusion_matrix_RandomForest = confusion_matrix(y_test,y_pred)

pd.DataFrame(confusion_matrix_RandomForest,columns = ['Predicciones 0','Predicciones 1'],index = ['Real 0','Real 1'])

acc_RandomForest  = accuracy_score(y_test,y_pred)
f1_RandomForest   = f1_score(y_test,y_pred)
prec_RandomForest = precision_score(y_test,y_pred)
rec_RandomForest  = recall_score(y_test,y_pred)
auc_RandomForest = roc_auc_score(y_test,y_pred_prob[:,1])

results = pd.DataFrame([['Random Forest',acc_RandomForest,f1_RandomForest,prec_RandomForest,rec_RandomForest,auc_RandomForest]],
                       columns = ['Modelo','Accuracy','F1','Precision','Recall','AUC'])

results

"""## xGBoost"""

#df_tcancer = pd.read_pickle('dataset_completotransformado.pkl')

# Separar características y target
X = df_tcancer.drop(columns='Stage')
y = df_tcancer['Stage']

# Dividir el dataset
X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify = y)
X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.2, random_state=42, stratify = y_temp)

X_train.shape, X_val.shape, X_test.shape, X_temp.shape

xgb = XGBClassifier(random_state=42)

# Entrenar el modelo (train + valid)
xgb.fit(X_temp, y_temp)
y_pred_train = xgb.predict(X_train)

# Calcular métricas
print('Train \n',classification_report(y_train, y_pred_train))

# Predecir con el conjunto de prueba
y_pred      = xgb.predict(X_test)
y_pred_prob = xgb.predict_proba(X_test)[:, 1]

# Calcular métricas
print('Test \n',classification_report(y_test, y_pred))

print('Test AUC: ',roc_auc_score(y_test, y_pred_prob))

from sklearn.metrics import confusion_matrix
confusion_matrix(y_test, y_pred)

"""# Optimización

## Regresión logística con hiperparámatros
"""

df_tcancer = pd.read_pickle('dataset_completotransformado.pkl')

# Separar las características y la variable objetivo
X = df_tcancer.drop(columns=['Stage'])
y = df_tcancer['Stage']

# Dividir los datos
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

param_grid = {
    'C': [0.01, 0.1, 1, 10, 100],  # Regularización, mayor C permite que el modelo se ajuste más
    'solver': ['lbfgs', 'liblinear', 'saga'],  # Métodos de optimización
    'penalty': ['l2', 'l1'],  # Regularización L2 y L1
    'class_weight': [None, 'balanced'],  # Balanceo de clases automático
    'max_iter': [100, 200, 500]  # Aumentar el número de iteraciones
}

# Configurar el modelo base
logistic_model = LogisticRegression(class_weight='balanced')

grid_search = GridSearchCV(
    estimator=logistic_model,
    param_grid=param_grid,
    scoring='roc_auc',  # Cambia el enfoque a mejorar el AUC
    cv=5,  # 5-fold cross-validation
    verbose=1,
    n_jobs=-1  # Usa todos los núcleos disponibles
)

# Ajustar el modelo con los datos de entrenamiento
grid_search.fit(X_train, y_train)

# Obtener los mejores hiperparámetros
print("Mejores hiperparámetros:", grid_search.best_params_)
print("Mejor puntuación (recall):", grid_search.best_score_)

# Predicciones en el conjunto de prueba
y_pred = grid_search.best_estimator_.predict(X_test)
y_pred_proba = grid_search.best_estimator_.predict_proba(X_test)[:, 1]

# Reporte de clasificación
print("Reporte de clasificación:")
print(classification_report(y_test, y_pred))

# Calcular y mostrar el AUC
auc = roc_auc_score(y_test, y_pred_proba)
print("ROC-AUC en prueba:", auc)

from sklearn.metrics import confusion_matrix
confusion_matrix(y_test, y_pred)
#

"""## Random Forest con hiperparámetros"""

df_tcancer = pd.read_pickle('dataset_completotransformado.pkl')

# Separar características y target
X = df_tcancer.drop(columns='Stage')
y = df_tcancer['Stage']

# Dividir el conjunto de datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42,stratify=y)

# Configurar el modelo de Random Forest
random_forest = RandomForestClassifier(random_state=42)

# Definir la cuadrícula de hiperparámetros

param_grid = {
    'n_estimators'     : [20, 30, 50, 100, 200],       # Número de árboles en el bosque
    'max_depth'        : np.arange(5, 12, 2),  # Profundidad máxima del árbol
    'min_samples_split': [5, 10],              # Mínimo número de muestras para dividir un nodo
    'min_samples_leaf' : [1, 2, 4, 5],         # Mínimo número de muestras en un nodo hoja
    'max_features'     : ['sqrt',None],        # Número de características a considerar al buscar la mejor división
    'bootstrap'        : [True, False],        # Uso de bootstrapping
    'criterion'        : ['gini','entropy'],   # Mínimo número de muestras para dividir un nodo
    'class_weight'     : [None, 'balanced']
    }

#param_grid = {
#    'n_estimators': [50, 100, 200],
#    'max_depth': [10, 20, None],
#    'min_samples_split': [2, 5],
#    'min_samples_leaf': [1, 2],
#    'max_features': ['sqrt', None],
#    'bootstrap': [True],
#    'criterion': ['gini', 'entropy'],
#    'class_weight': ['balanced']
#}

# Configurar RandomizedSearchCV


#Configurar RandomizedSearchCV
rf = RandomizedSearchCV(
        estimator  = random_forest,
        param_distributions = param_grid ,
        cv = 5,
        n_iter = 100,
        n_jobs = -1,
        verbose = 1,
        scoring = 'recall',
        random_state = 42
      )


#rf = RandomizedSearchCV(
#    estimator=random_forest,
#    param_distributions= param_grid,
#    cv=5,
#    n_iter=150,  # Más iteraciones
#    n_jobs=-1,
#    verbose=2,
#    scoring='roc_auc',  # Métrica mejorada
#    random_state=42
#)

# Ajustar el modelo a los datos de entrenamiento
rf.fit(X_train, y_train)

# Ver classification report TRAIN
y_pred_train = rf.predict(X_train)

# Calcular métricas
print('Train \n',classification_report(y_train, y_pred_train))

# Obtener los mejores parámetros y el mejor puntaje
best_params = rf.best_params_
best_score  = rf.best_score_

print(f"Mejores parámetros: {best_params}")
print(f"Mejor puntaje: {best_score}")

# Obtener el mejor modelo
best_rf = rf.best_estimator_

#Predict xTest
y_pred = best_rf.predict(X_test)

# Calcular la métrica recall

# Predecir con el conjunto de prueba
y_pred      = best_rf.predict(X_test)
y_pred_prob = best_rf.predict_proba(X_test)[:, 1]

# Calcular métricas
print('Test \n',classification_report(y_test, y_pred))

print('Test AUC: ',roc_auc_score(y_test, y_pred_prob))

from sklearn.metrics import confusion_matrix
confusion_matrix(y_test, y_pred)

"""## xGBoost con hiperparámetros"""

df_tcancer = pd.read_pickle('dataset_completotransformado.pkl')

X = df_tcancer.drop('Stage', axis=1)
y = df_tcancer['Stage']

X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify = y)
X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.2, random_state=42, stratify = y_temp)

class_distribution = Counter(y_train)
scale_pos_weight = class_distribution[0] / class_distribution[1]  # Ajusta según

param_grid = {
    'n_estimators': [50, 100, 200, 300],
    'learning_rate': [0.01, 0.02, 0.05, 0.1],
    'max_depth': [3, 5, 7, 10],
    'min_child_weight': [1, 3, 5],
    'colsample_bytree': [0.6, 0.8, 1.0],
    'gamma': [0, 0.1, 0.2],
    'reg_alpha': [0, 0.5, 1],
    'reg_lambda': [1, 1.5, 2],
    'subsample': [0.6, 0.8, 1.0],
    'scale_pos_weight': [1, scale_pos_weight],  # Incluye balance dinámico
    'objective': ['binary:logistic'],
    'eval_metric': ['auc']
}

xgb = XGBClassifier(
    objective='binary:logistic',   # Para clasificación binaria
   # eval_metric='auc',             # Métrica a utilizar
    use_label_encoder=False,       # Para evitar advertencias de la versión de XGBoost
    early_stopping_rounds=10,      # Detener el entrenamiento si no hay mejora en 10 iteraciones
    random_state=42
)

xg_search = RandomizedSearchCV(
    estimator=xgb,
    param_distributions=param_grid,
    scoring='recall',  # O prueba con 'roc_auc' o 'f1'
    n_iter=100,
    cv=5,
    verbose=1,
    random_state=42
)

xg_search.fit(X_train, y_train,
              eval_set=[(X_train, y_train), (X_val, y_val)])

# Obtener los mejores parámetros y el mejor puntaje
best_params = xg_search.best_params_
print(f"Mejores parámetros: {best_params}")

# Predecir  (train)
y_pred_train = xg_search.predict(X_train)

# Calcular métricas
print('Train \n',classification_report(y_train, y_pred_train))

# Predecir con el conjunto de validacion
y_pred      = xg_search.predict(X_val)
y_pred_prob = xg_search.predict_proba(X_val)[:, 1]

# Calcular métricas
print('Val \n',classification_report(y_val, y_pred))

print('Val AUC: ',roc_auc_score(y_val, y_pred_prob))

#Entrenar con todos los datos el mejor modelo
# Crear un modelo con los mejores parametros
xg_search_best = XGBClassifier(**best_params, early_stopping_rounds=10, random_state=42)
# Entrenar con todos los datos
#xg_search_best.fit(X_temp , y_temp)
# Ajustar el modelo
xg_search_best.fit(X_temp, y_temp,
              eval_set=[(X_temp, y_temp)])
              #eval_set=[(X_val, y_val)], verbose=True)

# Predecir con el conjunto de Train+Valid
y_pred      = xg_search_best.predict(X_temp)
y_pred_prob = xg_search_best.predict_proba(X_temp)[:, 1]

# Calcular métricas
print('Train+Valid \n',classification_report(y_temp, y_pred))

print('Train+Valid AUC: ',roc_auc_score(y_temp, y_pred_prob))

from sklearn.metrics import confusion_matrix
confusion_matrix(y_temp, y_pred)

#Predict xTest
y_pred = xg_search_best.predict(X_test)
y_pred_prob = xg_search_best.predict_proba(X_test)[:, 1]

# Calcular métricas
print('Test \n',classification_report(y_test, y_pred))

print('Test AUC: ',roc_auc_score(y_test, y_pred_prob))

from sklearn.metrics import confusion_matrix
confusion_matrix(y_test, y_pred)
#