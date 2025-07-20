# End-to-End MLOps Pipeline for Diabetes Prediction

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.9+-blue.svg?style=for-the-badge)](https://www.python.org/downloads/)

This repository contains the source code for a complete, end-to-end MLOps project. The goal is to build a robust, automated pipeline that ingests data, preprocesses it, trains a machine learning model, and deploys it as a web application on Google Cloud.

## 🌟 Features

* **Automated CI/CD:** The entire pipeline is automated using Jenkins, triggered by a `git push` to the main branch.
* **Cloud Integration:** Uses Google Cloud Storage (GCS) for data persistence and Google Container Registry (GCR) for storing Docker images.
* **Experiment Tracking:** All model training runs are tracked with MLflow, logging parameters, metrics, and model artifacts.
* **Containerization:** The final application is containerized using Docker for portability and consistent deployment.
* **Web Application:** A user-friendly web interface built with Flask to interact with the trained model.
* **Modular Code:** The project is structured as an installable Python package with clear separation of concerns.

## 🛠️ Tech Stack

| Tool                   | Purpose                                                        |
| ---------------------- | -------------------------------------------------------------- |
| **GitHub** | Version Control & CI/CD Trigger                                |
| **Jenkins** | CI/CD Automation & Orchestration                               |
| **Docker** | Containerization                                               |
| **Google Cloud Platform**| Data Storage (GCS), Container Registry (GCR), Deployment (Cloud Run) |
| **MLflow** | Experiment Tracking & Model Management                         |
| **Flask** | Web Framework for the User Application                         |
| **Python** | Core Programming Language                                      |
| **Scikit-learn & LightGBM**| Machine Learning Libraries                                     |

## 🏗️ Project Architecture

The pipeline follows a standard CI/CD workflow. A `git push` triggers a Jenkins job that automatically runs the entire process, from data ingestion to live deployment on Google Cloud Run.

Find the architecture here: https://n7kadda.github.io/diagrams/

---

## 🚀 Getting Started: Local Setup and Pipeline Execution

This guide will walk you through setting up the entire environment from scratch on your local machine.

### Prerequisites

* **Docker Desktop:** Ensure Docker Desktop is installed and running in the background.
* **GCP Account:** A Google Cloud Platform account with a project created and billing enabled.
* **GitHub Account:** A GitHub account and a personal access token with `repo` permissions.

### Step 1: Set Up the Custom Jenkins Container

Our pipeline requires a special Jenkins environment that has Docker and other tools installed inside it. We'll build this using a custom Dockerfile.

1.  **Create the Jenkins Dockerfile:**
    * In your project's root directory, create a new folder named `custom_jenkins`.
    * Inside it, create a file named `Dockerfile`.
    * Paste the following content into this `Dockerfile`:
        ```dockerfile
        # Use the Jenkins image as the base image
        FROM jenkins/jenkins:lts

        # Switch to root user to install dependencies
        USER root

        # Install prerequisites and Docker
        RUN apt-get update -y && \
            apt-get install -y apt-transport-https ca-certificates curl gnupg software-properties-common && \
            curl -fsSL [https://download.docker.com/linux/debian/gpg](https://download.docker.com/linux/debian/gpg) | apt-key add - && \
            echo "deb [arch=amd64] [https://download.docker.com/linux/debian](https://download.docker.com/linux/debian) bullseye stable" > /etc/apt/sources.list.d/docker.list && \
            apt-get update -y && \
            apt-get install -y docker-ce docker-ce-cli containerd.io && \
            apt-get clean

        # Add Jenkins user to the Docker group
        RUN groupadd -f docker && \
            usermod -aG docker jenkins

        # Switch back to the Jenkins user
        USER jenkins
        ```

2.  **Build and Run the Jenkins Container:**
    * Open a terminal and navigate into the `custom_jenkins` folder:
        ```bash
        cd custom_jenkins
        ```
    * Build the custom Jenkins image:
        ```bash
        docker build -t jenkins-dind .
        ```
    * Run the container. This command allows Jenkins to run Docker commands (Docker-in-Docker).
        ```bash
        # For Windows (PowerShell)
        docker run -d --name jenkins-dind --privileged -p 8080:8080 -p 50000:50000 -v /var/run/docker.sock:/var/run/docker.sock -v jenkins_home:/var/jenkins_home jenkins-dind
        
        # For Mac/Linux
        docker run -d --name jenkins-dind --privileged -p 8080:8080 -p 50000:50000 -v /var/run/docker.sock:/var/run/docker.sock -v jenkins_home:/var/jenkins_home jenkins-dind
        ```

3.  **Initial Jenkins Setup:**
    * Check that the container is running: `docker ps`
    * Get the initial admin password from the logs:
        ```bash
        docker logs jenkins-dind
        ```
    * Copy the password from the output.
    * Navigate to `http://localhost:8080` in your browser, paste the password, and follow the setup instructions. **Install suggested plugins** and create your admin user.

### Step 2: Install Additional Tools in the Jenkins Container

We need to install Python and the Google Cloud SDK inside our running Jenkins container.

1.  **Open a shell inside the container as root:**
    ```bash
    docker exec -u root -it jenkins-dind bash
    ```

2.  **Install Python:**
    ```bash
    apt-get update -y
    apt-get install -y python3 python3-pip python3-venv
    ln -s /usr/bin/python3 /usr/bin/python # Create a symlink
    exit
    ```

3.  **Install Google Cloud SDK:**
    * Open another shell in the container as root:
        ```bash
        docker exec -u root -it jenkins-dind bash
        ```
    * Run the installation commands:
        ```bash
        apt-get install -y curl apt-transport-https ca-certificates gnupg
        curl [https://packages.cloud.google.com/apt/doc/apt-key.gpg](https://packages.cloud.google.com/apt/doc/apt-key.gpg) | apt-key add -
        echo "deb [https://packages.cloud.google.com/apt](https://packages.cloud.google.com/apt) cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
        apt-get update && apt-get install -y google-cloud-sdk
        exit
        ```

4.  **Restart the container** for all changes to take effect:
    ```bash
    docker restart jenkins-dind
    ```

### Step 3: Configure the Jenkins Pipeline

1.  **Log in** to your Jenkins dashboard at `http://localhost:8080`.
2.  **Create Credentials:**
    * Go to `Manage Jenkins` > `Credentials`.
    * Add your **GitHub personal access token** (with `repo` permissions) as a "Secret text" credential. Give it an ID like `github-token`.
    * Add your **GCP service account JSON key** as a "Secret file" credential. Give it an ID like `gcp-key`.
3.  **Create the Pipeline Job:**
    * Click "New Item" on the dashboard.
    * Enter a name (e.g., `diabetes-pipeline`), select "Pipeline", and click OK.
    * Under the "Pipeline" section, select "Pipeline script from SCM".
    * **SCM:** Select "Git".
    * **Repository URL:** Enter the URL of your GitHub repository.
    * **Credentials:** Select the `github-token` credential you created.
    * **Script Path:** Ensure it is set to `Jenkinsfile`.
4.  **Save and Run:** Click "Save", and then click "Build Now" to run your first pipeline!

## 🤝 Contributing

Contributions are welcome! If you have suggestions for improvements or find any issues, please feel free to open an issue or submit a pull request.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## 📜 License

This project is distributed under the MIT License.