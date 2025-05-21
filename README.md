# Setting up a CI/CD Pipeline for Automated Deployment

This project demonstrates a complete CI/CD workflow for deploying a machine learning web application using **GitHub Actions** and **Docker**. The app is automatically built and tested on every push to the repository.

---

## Project Overview

- **Goal**: Set up a CI/CD pipeline that automates the process of building, testing, and deploying a containerized application.
- **App**: A simple Streamlit app that predicts customer churn using a pre-trained ML model.
- **CI/CD**: Implemented using GitHub Actions to build and optionally deploy Docker images.
- **Containerization**: Ensures the app runs consistently across different environments.

---

## CI/CD Workflow

### Trigger:
Runs automatically on every push to the `main` branch.

### Steps:
1. **Checkout** the code.
2. **Set up Python** environment.
3. **Build Docker image** of the app.

### GitHub Actions Workflow (`.github/workflows/deploy.yml`)

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Set up Docker
      run: |
        sudo apt-get update
        sudo apt-get install -y docker.io

    - name: Build Docker image
      run: docker build -t churn-app .

