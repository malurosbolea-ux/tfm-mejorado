import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder, StandardScaler
import pickle

print("=" * 50)
print("  VALORALIA — Entrenamiento con datos REALES")
print("=" * 50)

# 1. Cargar datos reales
df = pd.read_csv('datos_inmobiliarios_madrid.csv')
print(f"\n✅ Dataset cargado: {len(df):,} inmuebles reales")

# 2. Feature engineering (mismo que NB2)
estado_map = {'A reformar': 0, 'Buen estado': 1, 'Obra nueva': 2}
df['estado_cod'] = df['estado'].map(estado_map).fillna(1).astype(int)

def codificar_planta(planta):
    planta = str(planta).lower()
    if 'bajo' in planta or 'sótano' in planta:
        return 0
    elif 'entre' in planta:
        return 1
    else:
        try:
            return min(int(''.join(filter(str.isdigit, planta))), 10)
        except:
            return 2

df['planta_cod'] = df['planta'].apply(codificar_planta)

le_municipio = LabelEncoder()
df['municipio_cod'] = le_municipio.fit_transform(df['municipio'])

le_calef = LabelEncoder()
df['calefaccion_cod'] = le_calef.fit_transform(df['calefaccion'])

for col in ['tiene_ascensor', 'tiene_terraza', 'tiene_trastero']:
    df[col] = df[col].astype(int)

df['ratio_hab_m2'] = df['habitaciones'] / df['tamano_m2']
df['ratio_banos_hab'] = df['banos'] / df['habitaciones'].replace(0, 1)

# 3. Definir features
FEATURES = [
    'tamano_m2', 'habitaciones', 'banos', 'planta_cod',
    'tiene_ascensor', 'tiene_terraza', 'tiene_trastero',
    'calefaccion_cod', 'estado_cod', 'municipio_cod',
    'ratio_hab_m2', 'ratio_banos_hab'
]
TARGET = 'precio_actual'

X = df[FEATURES]
y = df[TARGET]

# 4. Normalizar
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 5. Entrenar
print("🌲 Entrenando Random Forest (200 estimadores)...")
model = RandomForestRegressor(
    n_estimators=200, max_depth=20, min_samples_leaf=5,
    random_state=42, n_jobs=-1
)
model.fit(X_scaled, y)

# 6. Guardar TODO en un solo archivo
paquete = {
    'model': model,
    'scaler': scaler,
    'le_municipio': le_municipio,
    'le_calefaccion': le_calef,
    'features': FEATURES,
    'municipios': list(le_municipio.classes_),
    'calefacciones': list(le_calef.classes_),
    'estados': ['A reformar', 'Buen estado', 'Obra nueva'],
    'n_registros': len(df),
    'precio_medio': float(df[TARGET].mean()),
}

with open('valoralia_production.pkl', 'wb') as f:
    pickle.dump(paquete, f)

print(f"✅ Modelo entrenado con {len(df):,} registros reales")
print(f"   Municipios: {list(le_municipio.classes_)}")
print(f"   Precio medio: {df[TARGET].mean():,.0f}€")
print(f"💾 Guardado: valoralia_production.pkl")
