<div align="center">

# VALORALIA — Sistema de Valoración Inmobiliaria con IA

### Trabajo Fin de Máster · Big Data e Inteligencia Artificial
### Universidad CEU San Pablo · 2025/2026

**Autora:** María Luisa Ros Bolea  
**Tutor:** Miguel Sánchez Novo

---

`Random Forest` · `Transfer Learning (ResNet50)` · `Explainable AI` · `Stress Testing` · `AWS EC2` · `Streamlit`

</div>

---

## Descripción del proyecto

**VALORALIA** es un sistema de valoración automatizada de inmuebles (AVM) para el mercado de la Comunidad de Madrid. El proyecto aborda dos preguntas fundamentales:

1. ¿Se puede predecir con precisión el precio de un inmueble a partir de sus características tabulares (superficie, ubicación, estado...)?
2. ¿Mejora esa predicción si incorporamos información visual extraída de fotografías del interior mediante redes neuronales convolucionales?

El sistema integra un pipeline completo de ciencia de datos: desde la ingestión del dato bruto hasta el despliegue en producción en AWS EC2, pasando por entrenamiento, explicabilidad (XAI) y simulación de escenarios de crisis financiera.

## Resultados principales

| Modelo | Registros | MAE | R² | MAPE |
|--------|-----------|-----|-----|------|
| **Baseline tabular (RF)** | 12.500 | 12.646 € | 0.9644 | 5.70% |
| Híbrido (tabular + CNN + PCA) | 300 | 16.660 € | 0.9480 | — |

### Validación contra mercado real (2.500 registros de test)

- **84.2%** de predicciones con error < 10%
- **97.6%** de predicciones con error < 20%
- Mejor municipio: Getafe (MAE: 11.407€) · Peor: Alcorcón (MAE: 13.327€)

> **Nota sobre el componente visual:** La integración de features extraídas con ResNet50 + PCA se presenta como demostración metodológica de un pipeline multimodal completo. Con solo 300 imágenes sin vinculación verificada imagen-inmueble, el modelo híbrido no supera al baseline tabular. Sin embargo, la arquitectura está validada y lista para escalar con un dataset de imágenes más amplio y correctamente mapeado. Se discuten las implicaciones y líneas futuras en la memoria.

## Arquitectura del repositorio

```
tfm-mejorado/
├── Notebooks/                    # Pipeline de ciencia de datos (7 módulos)
│   ├── NB1_Ingestion_Datos.ipynb
│   ├── NB2_Preprocesamiento.ipynb
│   ├── NB3_Entrenamiento_Modelo_Hibrido.ipynb
│   ├── NB4_Interfaz_Tasacion.ipynb
│   ├── NB5_XAI_Explicabilidad.ipynb
│   ├── NB6_Stress_Test.ipynb
│   └── V2_Validacion_Mercado.ipynb
│
├── Data/
│   ├── Raw/                      # Dataset original (12.500 inmuebles)
│   └── Processed/                # Datos transformados, splits train/test
│
├── Models/                       # Modelos serializados (.pkl)
├── Reports/                      # Gráficos y métricas exportadas
├── APP_DEPLOY/                   # Código de producción (Streamlit + Docker)
└── README.md
```

> **Archivos pesados (imágenes, modelos .h5):** disponibles en el [Google Drive del proyecto](https://drive.google.com/drive/folders/1Xnua1f5f0NBkgiPSVIrbQ7pwlL4AkzEj?usp=share_link) por limitaciones de tamaño de GitHub.

## Pipeline de notebooks

| # | Notebook | Descripción |
|---|----------|-------------|
| 1 | **Ingestión de datos** | Carga del dataset de 12.500 inmuebles, auditoría de calidad, inventario de imágenes |
| 2 | **Preprocesamiento** | Feature engineering (12 variables), normalización, split train/test estratificado |
| 3 | **Entrenamiento híbrido** | Baseline tabular (RF) + extracción de features con ResNet50 + PCA + modelo combinado |
| 4 | **Interfaz de tasación** | Motor de valoración con lógica anti-alucinación y simulador de escenarios macro |
| 5 | **XAI — Explicabilidad** | Permutation Importance, Partial Dependence Plots, Grad-CAM sobre imágenes |
| 6 | **Stress Testing** | Simulación de crisis (-20%), detección de concept drift, re-entrenamiento |
| V2 | **Validación de mercado** | Contraste de predicciones con precios reales, análisis por municipio y rango |

## Stack tecnológico

- **Lenguaje:** Python 3.10+
- **ML:** scikit-learn (Random Forest, Gradient Boosting, PCA)
- **Deep Learning:** TensorFlow / Keras (ResNet50, Grad-CAM)
- **Visualización:** Matplotlib, Seaborn
- **Despliegue:** Streamlit, Docker, AWS EC2
- **Datos:** pandas, NumPy

## Despliegue en producción

La aplicación está desplegada en una instancia AWS EC2 como contenedor Docker con Streamlit.

```bash
# Reproducir localmente
cd APP_DEPLOY
pip install -r requirements.txt
streamlit run app.py
```

## Contacto

**María Luisa Ros Bolea**  
📧 malurosbolea@gmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/maría-luisa-ros-bolea-400780160/)  
🌐 [Portfolio](https://malurosbolea-ux.github.io/digital-strategy-portfolio/)  
