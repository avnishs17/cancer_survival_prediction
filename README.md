# Cancer Survival Prediction MLOps Pipeline

A complete MLOps solution for cancer survival prediction using Machine Learning with DagHub integration, Kubeflow pipelines, and Flask deployment.

## Project Architecture

```
cancer_survival_prediction/
├── src/
│   ├── data_preprocessing.py    # Data processing pipeline
│   ├── model_training.py        # Model training with DagHub integration
│   ├── logger.py               # Logging configuration
│   └── custom_exception.py     # Custom exception handling
├── kubeflow_pipeline/
│   └── mlops_pipeline.py       # Kubeflow pipeline definition
├── templates/                  # Flask HTML templates
├── static/                     # Static web assets
├── artifacts/                  # Generated artifacts (models, data)
├── app.py                     # Flask web application
├── Dockerfile                 # Container configuration
├── requirements.txt           # Python dependencies
└── mlops_pipeline.yaml        # Generated Kubeflow pipeline YAML
```

## Technology Stack

- **ML Framework**: Scikit-learn, MLflow
- **Orchestration**: Kubeflow Pipelines
- **Experiment Tracking**: DagHub + MLflow
- **Version Control**: Git + DagHub Repository Integration
- **Containerization**: Docker + Docker Hub
- **Web Framework**: Flask
- **Infrastructure**: Kubernetes (Minikube)

## Environment Setup

### 1. Python Environment

```powershell
# Create virtual environment
python -m venv env

# Activate environment (Windows)
.\env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install package in development mode
pip install -e .
```

### 2. Minikube Installation (Windows PowerShell as Admin)

```powershell
# Create minikube directory
New-Item -Path 'c:\' -Name 'minikube' -ItemType Directory -Force

# Download minikube
$ProgressPreference = 'SilentlyContinue'
Invoke-WebRequest -OutFile 'c:\minikube\minikube.exe' -Uri 'https://github.com/kubernetes/minikube/releases/latest/download/minikube-windows-amd64.exe' -UseBasicParsing

# Add to system PATH
$oldPath = [Environment]::GetEnvironmentVariable('Path', [EnvironmentVariableTarget]::Machine)
if ($oldPath.Split(';') -inotcontains 'C:\minikube'){
  [Environment]::SetEnvironmentVariable('Path', $('{0};C:\minikube' -f $oldPath), [EnvironmentVariableTarget]::Machine)
}

# Start cluster
minikube start
```

### 3. Kubectl Installation

```powershell
# Download kubectl
curl.exe -LO "https://dl.k8s.io/release/v1.33.0/bin/windows/amd64/kubectl.exe"

# Verify installation
kubectl version --client
```

### 4. Kubeflow Pipelines Setup

```powershell
# Set pipeline version
$env:PIPELINE_VERSION="2.4.0"

# Deploy Kubeflow Pipelines
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$env:PIPELINE_VERSION"
kubectl wait --for condition=established --timeout=60s crd/applications.app.k8s.io
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/env/platform-agnostic?ref=$env:PIPELINE_VERSION"

# Verify deployment and # wait till all pods are running before running next command
kubectl get pod -A

# Port forward to access UI
kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8080:80
```

Access Kubeflow UI: http://localhost:8080

## Git Version Control & DagHub Repository

### 1. Initialize Git Repository and Push to GitHub

```powershell
# Initialize git repository
git init

# Add all files
git add .

# Initial commit
git commit -m "Initial cancer survival prediction project"

# Create repository on GitHub first (github.com)
# Then add GitHub as remote origin
git remote add origin https://github.com/your_github_username/cancer_survival_prediction.git

# Push code to GitHub
git push -u origin main
```

### 2. Import GitHub Repository to DagHub

1. Go to [dagshub.com](https://dagshub.com) and create account
2. Click "Create Repository" 
3. Name it `cancer` (must match MLflow tracking URI)
4. Choose "Import from GitHub"
5. Give DagHub permission to access your GitHub repository
6. Select your GitHub repository: `your_github_username/cancer_survival_prediction`
7. DagHub will automatically sync with your GitHub repository

### 3. Git Workflow for Continuous Development

```powershell
# Make changes to code
git add .
git commit -m "Update model parameters"

# Push to GitHub (DagHub will automatically sync)
git push origin main
```

### 4. Verify DagHub Integration

- Check DagHub repository: `https://dagshub.com/your_username/cancer`
- Verify code sync from GitHub
- Confirm MLflow tracking is enabled

**Note**: DagHub imports and syncs with your GitHub repository. This provides seamless integration where you push code to GitHub and DagHub automatically tracks experiments and manages ML projects with version correlation.

## Docker Optimization

### 1. Docker Ignore Configuration

The `.dockerignore` file prevents unnecessary files from being included in Docker images:

```ignore
venv/*
env/*
cancer_survival.egg-info
logs/*
__pycache__/*
```

### 2. Git Ignore Configuration

The `.gitignore` file keeps unnecessary files out of version control:

```ignore
venv/*
env/*
cancer_survival.egg-info
logs/*
__pycache__/*
```

### 3. Optimized Docker Build

```powershell
# Build optimized image (excludes files from .dockerignore)
docker build -t cancer_survival:latest .

# Check image size
docker images cancer_survival:latest
```

## DagHub Integration

### 1. DagHub Setup

After importing your GitHub repository to DagHub (as described in Git section above):

1. Go to your DagHub repository: `https://dagshub.com/your_username/cancer`
2. Navigate to Settings → Access Tokens 
3. Use the **default token** provided by DagHub (don't generate a new one)
4. Copy the default token value
5. Note your username and the default token

### 2. Local Environment Variables

```powershell
# Set environment variables (Windows) - use DagHub default token
set $env:DAGSHUB_USERNAME="your_username"
set $env:DAGSHUB_USER_TOKEN="your_default_dagshub_token"
```

### 3. DagHub Integration in Model Training

The `model_training.py` automatically configures DagHub integration:

```python
# Configure MLflow to use DagHub tracking server
dagshub_username = os.getenv("DAGSHUB_USERNAME")
dagshub_token = os.getenv("DAGSHUB_USER_TOKEN")

if dagshub_username and dagshub_token:
    # Set MLflow tracking URI to DagHub
    mlflow.set_tracking_uri(f"https://dagshub.com/{dagshub_username}/cancer.mlflow")
    
    # Set authentication environment variables
    os.environ["MLFLOW_TRACKING_USERNAME"] = dagshub_username
    os.environ["MLFLOW_TRACKING_PASSWORD"] = dagshub_token
```

### 4. Running Model Training with DagHub

```powershell
# Ensure environment variables are set
python src/model_training.py
```

Experiments will be tracked at: `https://dagshub.com/{your_username}/cancer.mlflow`

## Docker Containerization

### 1. Build Optimized Docker Image

```powershell
# Build image (automatically excludes files from .dockerignore)
docker build -t cancer_survival:latest .

# Test locally
docker run -p 5000:5000 cancer_survival:latest
```

### 2. Push to Docker Hub (Required for Kubeflow)

```powershell
# Login to Docker Hub
docker login

# Tag image with your Docker Hub username
docker tag cancer_survival:latest your_dockerhub_username/cancer_survival:latest

# Push image (this image will be used by Kubeflow pipeline)
docker push your_dockerhub_username/cancer_survival:latest
```

**Important**: The Docker image pushed to Docker Hub is used by Kubeflow pipeline components. Update the image name in `kubeflow_pipeline/mlops_pipeline.py` to match your Docker Hub repository.

## Kubeflow Pipeline Deployment

### 1. Configure DagHub Secrets in Kubernetes

```powershell
# Delete existing secret (if any)
kubectl delete secret dagshub-secret -n kubeflow --ignore-not-found

# Create new secret with DagHub credentials (use default token)
kubectl create secret generic dagshub-secret `
  --from-literal=DAGSHUB_USERNAME=your_username `
  --from-literal=DAGSHUB_USER_TOKEN=your_default_dagshub_token `
  -n kubeflow
```

### 2. Generate Pipeline YAML

```powershell
# Update Docker image name in kubeflow_pipeline/mlops_pipeline.py
# Change "avnishsingh17/cancer_survival:latest" to "your_dockerhub_username/cancer_survival:latest"

# Generate Kubeflow pipeline YAML
python kubeflow_pipeline/mlops_pipeline.py
```

This creates `mlops_pipeline.yaml` file that references your Docker Hub image.

### 3. Deploy Pipeline to Kubeflow

1. Access Kubeflow UI: http://localhost:8080
2. Click "Upload pipeline"
3. Create new pipeline with name
4. Upload `mlops_pipeline.yaml` file
5. Click "Create"

### 4. Run Pipeline

1. Go to "Create run"
2. Click "Experiments" → Create new experiment
3. Select your pipeline
4. Choose "One-off" run type
5. Click "Start"

### 5. Pipeline Components

The pipeline includes two main components that run in Docker containers:

1. **Data Processing**: Preprocesses raw data, handles encoding, scaling
   - Uses Docker image: `your_dockerhub_username/cancer_survival:latest`
   - Command: `python src/data_preprocessing.py`

2. **Model Training**: Trains GradientBoosting model, logs metrics to DagHub
   - Uses Docker image: `your_dockerhub_username/cancer_survival:latest`
   - Command: `python src/model_training.py`

Both components have DagHub environment variables injected automatically via Kubernetes secrets.

## Local Development Workflow

### 1. Data Processing

```powershell
python src/data_preprocessing.py
```

Outputs:
- `artifacts/processed/X_train.pkl`
- `artifacts/processed/X_test.pkl` 
- `artifacts/processed/y_train.pkl`
- `artifacts/processed/y_test.pkl`
- `artifacts/processed/scaler.pkl`

### 2. Model Training

```powershell
# Ensure DagHub variables are set
python src/model_training.py
```

Outputs:
- `artifacts/models/model.pkl`
- MLflow experiment logged to DagHub

### 3. Web Application

```powershell
python app.py
```

Access at: http://localhost:5000

## Pipeline Architecture

### Data Flow

```
Raw Data → Data Processing → Feature Engineering → Model Training → Model Evaluation → Deployment
```

### DagHub Integration Points

1. **Code Versioning**: GitHub repository imported and auto-synced with DagHub
2. **Local Training**: Direct MLflow tracking to DagHub
3. **Kubeflow Pipeline**: Kubernetes secrets for authentication, Docker containers with DagHub integration
4. **Experiment Tracking**: All metrics, parameters, and artifacts logged with GitHub commit correlation

### Key Features

- **Automated Data Processing**: Handles categorical encoding, scaling, feature selection
- **Model Training**: GradientBoosting classifier with hyperparameter tracking
- **Evaluation Metrics**: Accuracy, Precision, Recall, F1-Score, ROC-AUC
- **Containerized Deployment**: Docker-based deployment ready for any environment
- **Orchestrated Pipelines**: Kubeflow for production-grade ML workflows
- **Experiment Tracking**: Complete experiment lineage with DagHub integration

## Monitoring and Troubleshooting

### Check Pipeline Status

```powershell
# Check Kubeflow pods
kubectl get pods -n kubeflow

# Check pipeline runs
kubectl get pods -n kubeflow | grep ml-pipeline
```

### View Logs

```powershell
# View specific pod logs
kubectl logs <pod-name> -n kubeflow

# Follow logs in real-time
kubectl logs -f <pod-name> -n kubeflow
```

### DagHub Debug

```powershell
# Verify environment variables (ensure using default DagHub token)
echo $env:DAGSHUB_USERNAME
echo $env:DAGSHUB_USER_TOKEN

# Test MLflow connection
python -c "import mlflow; print(mlflow.get_tracking_uri())"
```

## Production Considerations

1. **Resource Limits**: Configure CPU/memory limits in Kubeflow components
2. **Data Versioning**: Use DagHub for dataset versioning
3. **Model Registry**: Leverage MLflow model registry via DagHub
4. **Monitoring**: Set up alerts for pipeline failures
5. **Security**: Rotate DagHub tokens regularly
6. **Scaling**: Configure horizontal pod autoscaling for high throughput


## File Structure Details

- **artifacts/**: Generated during pipeline execution
  - `raw/`: Original datasets
  - `processed/`: Processed features and scalers
  - `models/`: Trained model artifacts
- **kubeflow_pipeline/**: Pipeline definitions and configurations
- **src/**: Core ML pipeline components
- **templates/**: Flask web interface templates
- **static/**: CSS, JS, images for web interface
- **.dockerignore**: Excludes unnecessary files from Docker builds
- **.gitignore**: Excludes files from Git version control
- **Dockerfile**: Container configuration that uses optimized layer caching

This setup provides a complete end-to-end MLOps solution with experiment tracking, pipeline orchestration, and deployment capabilities.
