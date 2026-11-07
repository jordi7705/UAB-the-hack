import pandas as pd
import matplotlib
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor

X_synthetic, y_synthetic = make_classification(
    n_samples=200,      # Número de filas (gran escala)
    n_features=25,         # Número total de columnas/variables
    n_informative=15,      # Variables que realmente tienen información útil
    n_redundant=5,         # Variables que son combinaciones lineales de las útiles (simula correlación)
    n_repeated=0,          # Variables duplicadas
    n_classes=8,           # Clasificación binaria
    weights=[0.2, 0.15, 0.15, 0.15, 0.1,0.1, 0.1, 0.05],    # Desbalanceo de clases 
    flip_y=0.05,           # % de ruido aleatorio (cambia la etiqueta para simular errores en datos reales)
)

column_names = [f"Criteri d'avaluació{i}" for i in range(X_synthetic.shape[1])]
df = pd.DataFrame(X_synthetic, columns=column_names)
df['target'] = y_synthetic

X = df.drop('target', axis=1)
y = df['target']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2, 
    random_state=42, 
    stratify=y # Mantiene la proporción de clases en ambos sets
)

model = RandomForestClassifier(n_estimators=100, max_depth=15, n_jobs=-1, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

