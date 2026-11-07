import pandas as pd
from sklearn.datasets import make_classification
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Generem les dades sintètiques utilitzant els pesos del jurat.
# "Valor per a les persones" (20%), "Prototip i usabilitat" (15%), etc.
X_synthetic, y_synthetic = make_classification(
    n_samples=200,      
    n_features=25,         
    n_informative=15,      
    n_redundant=5,         
    n_repeated=0,          
    n_classes=8,           
    weights=[0.20, 0.15, 0.15, 0.15, 0.10, 0.10, 0.10, 0.05],
    flip_y=0.05,
    random_state=42
)

column_names = [f"Criteri d'avaluació {i}" for i in range(X_synthetic.shape[1])]
df = pd.DataFrame(X_synthetic, columns=column_names)
df['target'] = y_synthetic

X = df.drop('target', axis=1)
y = df['target']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2, 
    random_state=42, 
    stratify=y 
)

# Sustituïm RandomForestClassifier per GaussianNB per millorar la rapidesa.
model = GaussianNB()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

