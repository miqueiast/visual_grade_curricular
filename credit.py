import streamlit as st
import pandas as pd
from xgboost import XGBClassifier
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_curve
import matplotlib.pyplot as plt

# Carregar o conjunto de dados
df = pd.read_csv("german_data_credit_cat.csv")

# Selecionar atributos relevantes e variável de destino
attr_significant = ["Status of existing checking account", "Credit history", "Purpose",
                    "Savings account/bonds", "Present employment since",
                    "Personal status and sex", "Property", "Other installment plans",
                    "Housing", "foreign worker", "Credit amount", "Age in years", "Duration in month"]
target_variable = ["Cost Matrix(Risk)"]
df = df[attr_significant + target_variable]

# Transformar variáveis categóricas em one-hot encoding
col_cat_names = ["Status of existing checking account", "Credit history", "Purpose",
                 "Savings account/bonds", "Present employment since",
                 "Personal status and sex", "Property", "Other installment plans",
                 "Housing", "foreign worker"]
df = pd.get_dummies(df, columns=col_cat_names, drop_first=True)

# Converter variável de destino em numérica
risk = {"Good Risk": 1, "Bad Risk": 0}
df["Cost Matrix(Risk)"] = df["Cost Matrix(Risk)"].map(risk)

# Dividir o conjunto de dados em conjunto de treinamento e teste
X = df.drop("Cost Matrix(Risk)", axis=1)
y = df["Cost Matrix(Risk)"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

# Reduzir dimensionalidade usando PCA
pca = PCA(n_components=16)
X_train_pca = pca.fit_transform(X_train)
X_test_pca = pca.transform(X_test)

# Treinar o modelo XGBoost
model = XGBClassifier()
model.fit(X_train_pca, y_train)

# Prever no conjunto de teste
y_pred = model.predict(X_test_pca)

# Avaliar desempenho do modelo
accuracy = accuracy_score(y_test, y_pred)
st.write("Acurácia do Modelo:", round(accuracy * 100, 2))

# Exibir curva ROC
st.subheader("Curva ROC")
y_pred_prob = model.predict_proba(X_test_pca)[:, 1]
fpr, tpr, thresholds = roc_curve(y_test, y_pred_prob)
plt.plot([0, 1], [0, 1], 'k--')
plt.plot(fpr, tpr)
plt.xlabel('Taxa de Falsos Positivos')
plt.ylabel('Taxa de Verdadeiros Positivos')
plt.title('Curva ROC')
st.pyplot()

# Exibir Feature Importances
st.subheader("Importância das Features")
feature_importances = pd.DataFrame({"Feature": X.columns, "Importance": model.feature_importances_})
feature_importances = feature_importances.sort_values(by="Importance", ascending=False)
st.table(feature_importances)

# Exibir exemplo de previsão
st.subheader("Exemplo de Previsão")
example_input = X_test.iloc[0]
example_prediction = model.predict([example_input])[0]
st.write("Entrada do Exemplo:", example_input)
st.write("Previsão para o Exemplo:", example_prediction)
