# CreditEase
This is a system aimed to achieve accurate predictions for mobile loans using a dataset from Kaggle.
# Project README

## Overview
In the rapidly evolving financial services sector, mobile loans have emerged as a popular solution for quick and convenient access to credit. However, the challenge lies in accurately assessing the creditworthiness of applicants to minimize default rates. This project explores the development of an intelligent system for predicting mobile loan eligibility using machine learning techniques. Utilizing real data from a Kenyan bank, the system aims to classify customers into those likely to default and those eligible for loans.

By analyzing customer data and employing predictive modeling, this system seeks to enhance the decision-making process for loan issuance. Additionally, we introduce a chatbot interface to interact with customers and collect relevant data, further improving the accuracy of loan eligibility predictions. The interactive chatbot technology presents a novel approach to modernizing financial services and promoting financial inclusion in underserved populations.

## Table of Contents
- [Introduction](#introduction)
- [Project Structure](#project-structure)
- [Data Description](#data-description)
- [Machine Learning Model](#machine-learning-model)
- [Chatbot Integration](#chatbot-integration)
- [Installation and Setup](#installation-and-setup)
- [Usage](#usage)
- [Results and Evaluation](#results-and-evaluation)
- [Future Work](#future-work)
- [Contributors](#contributors)
- [License](#license)

## Introduction
### Background
Mobile loans provide an accessible way for individuals to obtain credit, especially in regions with limited banking infrastructure. However, the ease of access also increases the risk of defaults. Traditional methods of credit assessment may not be sufficient to handle the large volume and unique characteristics of mobile loan applicants. Therefore, there is a need for an advanced system that can efficiently predict loan eligibility.

### Objectives
- Develop a machine learning model to predict mobile loan eligibility.
- Utilize customer data from a Kenyan bank to train and test the model.
- Implement a chatbot interface to interact with customers and gather additional data.
- Enhance the accuracy of loan eligibility predictions through continuous learning and data collection.

## Project Structure
The project is structured as follows:
```
mobile-loan-prediction/
├── data/
│   ├── raw/               # Raw data from the Kenyan bank
│   ├── processed/         # Processed data for modeling
│   └── external/          # Additional data sources
├── notebooks/             # Jupyter notebooks for data analysis and modeling
├── src/
│   ├── data/              # Scripts for data processing and cleaning
│   ├── features/          # Scripts for feature engineering
│   ├── models/            # Scripts for model training and evaluation
│   └── chatbot/           # Chatbot integration scripts
├── tests/                 # Unit tests for the project
├── reports/               # Generated reports and documentation
└── README.md              # Project README file
```

## Data Description
### Data Sources
The primary data source for this project is customer data from a Kenyan bank. The data includes:
- Demographic information (age, gender, etc.)
- Financial history (previous loans, repayment history, etc.)
- Mobile transaction data

### Data Processing
The data undergoes several preprocessing steps:
1. **Cleaning**: Handling missing values, outliers, and inconsistencies.
2. **Normalization**: Scaling numerical features to a standard range.
3. **Feature Engineering**: Creating new features that may enhance model performance.

## Machine Learning Model
### Model Selection
Several machine learning algorithms are explored, including:
- Logistic Regression
- Decision Trees
- Random Forests
- Gradient Boosting
- Neural Networks

### Training and Evaluation
The data is split into training and testing sets. Various evaluation metrics, such as accuracy, precision, recall, and F1-score, are used to assess model performance. Cross-validation is employed to ensure robustness.

### Hyperparameter Tuning
Hyperparameter tuning is performed using grid search and random search techniques to optimize model performance.

## Chatbot Integration
### Chatbot Framework
The chatbot is built using a conversational AI framework such as Rasa or Dialogflow. It interacts with customers to:
- Collect additional data
- Provide loan application status
- Answer common queries

### Data Collection
The chatbot collects data that may not be available in the initial dataset, such as current employment status or additional financial obligations. This data is used to improve the accuracy of the machine learning model.

## Installation and Setup
### Prerequisites
- Python 3.x
- Jupyter Notebook
- Virtual Environment

### Installation Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/mobile-loan-prediction.git
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
### Running the Model
1. Preprocess the data:
   ```bash
   python src/data/preprocess.py
   ```
2. Train the model:
   ```bash
   python src/models/train_model.py
   ```
3. Evaluate the model:
   ```bash
   python src/models/evaluate_model.py
   ```

### Running the Chatbot
1. Start the chatbot server:
   ```bash
   python src/chatbot/run_chatbot.py
   ```

## Results and Evaluation
The project reports include detailed analyses of model performance, feature importance, and the impact of the chatbot on data collection. Key findings and metrics are documented to provide insights into the effectiveness of the developed system.

## Future Work
- **Model Improvement**: Explore advanced machine learning techniques and ensemble methods.
- **Data Expansion**: Incorporate more diverse data sources for better generalization.
- **Chatbot Enhancements**: Improve the chatbot's conversational abilities and integration with other financial services.

## Contributors
- [Nicole](https://github.com/Swansong101) - Project Lead


## License
This project is licensed under the MIT License. See the LICENSE file for more details.
