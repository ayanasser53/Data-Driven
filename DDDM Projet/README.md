# Projet DDDM - Analyse E-commerce & Marketing

Ce projet est organise pour permettre a deux personnes de travailler en parallele sur Git avec une charge equilibree.

## Structure du projet

```text
DDDM Projet/
|
|-- analysis_business/
|   |-- notebooks/
|   |   `-- 01_analysis_business.ipynb
|   |-- reports/
|   `-- README.md
|
|-- ml_dashboard/
|   |-- notebooks/
|   |   `-- 02_ml_modeling.ipynb
|   |-- dashboard/
|   |   `-- app.py
|   |-- reports/
|   |   |-- AB_Test_Plan_DDDM.docx
|   |   `-- presentation_data_story.pdf
|   `-- README.md
|
|-- shared_data/
|   |-- Customers.csv
|   |-- data_Orders.csv
|   `-- README.md
|
|-- requirements.txt
|-- README.md
`-- .gitignore
```

## Repartition du travail

### Personne 1 - Analysis & Business

- Nettoyage et exploration des donnees.
- Analyse des clients, ventes, revenus et commandes.
- Creation des KPIs business.
- Segmentation client.
- Recommandations business.
- Redaction de la partie analyse du rapport.

Branche conseillee :

```bash
git checkout -b personne1-analysis-business
```

### Personne 2 - ML & Dashboard

- Preparation des features Machine Learning.
- Modeles predictifs : Logistic Regression, Decision Tree, Random Forest.
- Evaluation des modeles.
- SHAP / interpretabilite.
- Dashboard Streamlit.
- Plan A/B testing et presentation.

Branche conseillee :

```bash
git checkout -b personne2-ml-dashboard
```

## Installation

```bash
pip install -r requirements.txt
```

## Lancer le dashboard

```bash
python -m streamlit run ml_dashboard/dashboard/app.py
```

## Methode Git conseillee

Chaque personne travaille dans sa branche, puis fait une Pull Request vers `main`.

```bash
git add .
git commit -m "Describe the completed work"
git push origin nom-de-la-branche
```

## Donnees

Les datasets sont dans `shared_data/`. Les deux personnes peuvent les utiliser, mais il vaut mieux eviter de les modifier directement sans coordination.
