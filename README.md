# CloudTask-Pro 🚀

## Infrastructure as Code (IaC) with Azure DevOps and Terraform

# Project Overview

CloudTask-Pro is a cloud-based task management application deployed using modern DevOps practices.

This project demonstrates **Infrastructure as Code (IaC)** using Terraform, automated CI/CD using Azure DevOps, containerization using Docker, and cloud governance using Azure Policy.

CloudTask-Pro follows a 3-tier architecture consisting of a presentation layer, an application layer, and a data layer. For simplicity and cost efficiency, both the application and SQLite database are hosted within the same Docker container on a single Azure Linux Virtual Machine. In a production environment, the data tier would typically be hosted separately using a managed database service such as Azure SQL Database or Azure Database for PostgreSQL.

The complete workflow automates:

- Azure infrastructure provisioning
- Application containerization
- Docker image creation
- Image storage using Azure Container Registry
- Automated deployment to Azure Linux VM
- Cloud resource compliance enforcement

---

# Architecture Overview

# Architecture Overview

```text
                        +------------------+
                        |    Developer     |
                        +------------------+
                                 |
                                 | Push Code
                                 v
                        +------------------+
                        |      GitHub      |
                        +------------------+
                                 |
                                 | Trigger
                                 v
                  +-------------------------------+
                  |   Azure DevOps Pipeline        |
                  +-------------------------------+
                                 |
        +------------------------+-------------------------+
        |                        |                         |
        |                        |                         |
        v                        v                         v
+----------------+      +------------------+      +----------------------+
| Terraform Init | ---> | Terraform Plan   | ---> | Terraform Apply      |
+----------------+      +------------------+      +----------------------+
                                 |                         |
                                 |                         |
                                 |              Store Terraform State
                                 |                         |
                                 |                         v
                                 |              +----------------------+
                                 |              | Azure Storage Account|
                                 |              | (terraform.tfstate)  |
                                 |              +----------------------+
                                 |
                                 v
                   +--------------------------------+
                   | Azure Infrastructure           |
                   +--------------------------------+
                   | Resource Group                 |
                   | Virtual Network               |
                   | Subnet                        |
                   | Network Security Group        |
                   | Public IP                     |
                   | Linux Virtual Machine         |
                   +--------------------------------+
                                 |
                                 |
                                 v
                     +-----------------------+
                     | Docker Build Stage    |
                     +-----------------------+
                                 |
                                 |
                                 v
                   +---------------------------+
                   | Azure Container Registry  |
                   |          (ACR)            |
                   +---------------------------+
                                 |
                                 |
                                 v
                     +-----------------------+
                     | Deploy via SSH        |
                     +-----------------------+
                                 |
                                 |
                                 v
                     +-----------------------+
                     | Azure Linux VM        |
                     +-----------------------+
                                 |
                      Pull Latest Docker Image
                                 |
                                 v
                     +-----------------------+
                     | Docker Container      |
                     | CloudTask-Pro (Flask) |
                     +-----------------------+
                                 |
                                 |
                                 v
                     +-----------------------+
                     | End User              |
                     | http://<VM-IP>:5000  |
                     +-----------------------+
```

---

# Technologies Used

## Cloud Platform

- Microsoft Azure

## Infrastructure as Code

- Terraform

## CI/CD

- Azure DevOps Pipelines

## Containerization

- Docker

## Container Registry

- Azure Container Registry (ACR)

## Application

- Python
- Flask
- Flask-SQLAlchemy
- SQLite

## Version Control

- GitHub

---

# Project Features

CloudTask-Pro provides a task management dashboard.

Features:

✅ Add tasks  
✅ Search tasks  
✅ Mark tasks as completed  
✅ Delete tasks  
✅ Task statistics dashboard  
✅ Application health monitoring endpoint  

---

# Application Health Check

Endpoint:

```
GET /health
```

Response:

```json
{
  "status": "UP",
  "application": "CloudTask Pro",
  "version": "1.0"
}
```

---

# Repository Structure

```
CloudTask-Pro/

│
├── app/
│   ├── app.py
│   ├── database.py
│   ├── models.py
│   ├── requirements.txt
│   ├── templates/
│   └── static/
│
├── docker/
│   └── Dockerfile
│
├── terraform/
│   ├── provider.tf
│   ├── backend.tf
│   ├── main.tf
│   ├── network.tf
│   ├── vm.tf
│   ├── variables.tf
│   └── outputs.tf
│
├── azure-pipelines.yml
├── policy.json
├── README.md
└── .gitignore

```

---

# Terraform Infrastructure

Terraform provisions Azure infrastructure automatically.

Resources created:

## Azure Resource Group

```
cloudtask-rg
```

---

## Networking Components

Terraform creates:

- Virtual Network
- Subnet
- Network Security Group
- Public IP
- Network Interface


Network Security Rules:

| Port | Purpose |
|------|---------|
| 22 | SSH Access |
| 5000 | Flask Application |

---

## Azure Linux Virtual Machine

Terraform provisions:

- Ubuntu Server 22.04 LTS
- Azure Linux VM
- Network Interface
- Public IP
- Docker-ready environment

The VM hosts the CloudTask-Pro Docker container.

---

# Docker Configuration

The Flask application is containerized using Docker.

Docker workflow:

```
Python 3.11 Base Image
          |
          |
Install Dependencies
          |
          |
Copy Flask Application
          |
          |
Expose Port 5000
          |
          |
Run Flask Application
```

Build Docker image:

```bash
docker build -t cloudtask-pro .
```

Run container:

```bash
docker run -d -p 5000:5000 cloudtask-pro
```

---

# Azure DevOps CI/CD Pipeline

Pipeline workflow:

```
Developer Push
       |
       |
       v
Azure DevOps Pipeline

       |
       |
       +----------------+
       | Terraform      |
       |
       | terraform init |
       | validate       |
       | plan           |
       +----------------+

       |
       |
       v

Docker Build

       |
       |
       v

Azure Container Registry

       |
       |
       v

Deploy to VM

       |
       |
       v

Running Application
```

---

# Pipeline Stages

## Stage 1: Terraform

Purpose:

Validate infrastructure before deployment.

Commands:

```bash
terraform init

terraform validate

terraform plan
```

---

## Stage 2: Build

Actions:

- Build Docker image
- Tag image
- Push image to Azure Container Registry


Flow:

```
Application Code

        |

Docker Build

        |

Docker Image

        |

Azure Container Registry
```

---

## Stage 3: Deploy

Deployment steps:

1. Connect to Azure VM using SSH
2. Login to Azure Container Registry
3. Pull latest Docker image
4. Stop old container
5. Remove old container
6. Start new container

---

# Azure Policy Compliance

Azure Policy is used for cloud governance.

Policy:

```json
{
  "if": {
    "field": "tags",
    "exists": "false"
  },
  "then": {
    "effect": "deny"
  }
}
```

Purpose:

- Prevent untagged resources
- Enforce resource organization
- Improve Azure governance


Required tags:

```
Environment = Dev

Project = CloudTask
```

---

# Terraform State Management

Terraform state contains infrastructure information.

State files should not be committed to GitHub.

Do not upload:

```
terraform.tfstate
terraform.tfstate.backup
```

Recommended `.gitignore`:

```
.terraform/

*.tfstate

*.tfstate.*

*.tfvars

.env
```

---

# Running Terraform Locally

Initialize Terraform:

```bash
terraform init
```

Validate configuration:

```bash
terraform validate
```

Create deployment plan:

```bash
terraform plan
```

Deploy infrastructure:

```bash
terraform apply
```

Remove infrastructure:

```bash
terraform destroy
```

---

# Screenshots

The project documentation contains screenshots of:

- Azure Resource Group
- Terraform deployment
- Azure DevOps pipeline execution
- Docker deployment
- Azure Container Registry image
- Running CloudTask-Pro application

---

# Security Practices

Implemented:

✅ Azure DevOps secret variables  
✅ Terraform state protection  
✅ Azure Policy governance  
✅ Network security rules  
✅ Docker-based deployment  


Future improvements:

- Azure Storage backend for Terraform state
- Azure Key Vault integration
- HTTPS deployment
- Azure Monitor integration
- Automated testing stage
- Production approval gates

---

# Learning Outcomes

This project demonstrates:

- Infrastructure as Code
- Terraform automation
- Azure resource provisioning
- CI/CD pipeline implementation
- Docker container deployment
- Azure DevOps practices
- Cloud governance
- Linux VM administration

---

# Author

Sushrith Reddy Anyam

GitHub:

```
https://github.com/sushrithanyam
```
