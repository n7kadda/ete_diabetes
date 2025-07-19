pipeline{
    agent any

    environment{
        VENV_DIR = 'venv'
        GCP_PROJECT = 'abstract-gizmo-466207-e1'
        GCLOUD_PATH = '/var/jenkins_home/google-cloud-sdk/bin'
    }
    stages{
        stage('Clone Repository'){
            steps{
                script{
                    echo 'Cloning the repository...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/n7kadda/ete_diabetes.git']])
                }
            }
        }
        stage('Setting the venv and installing dependencies'){
            steps{
                script{
                    echo 'Setting the venv and installing dependencies...'
                    sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                }
            }
        }
        stage('Building and Pushing docker img to gcr'){
            steps{
                withCredentials([file(credentialsId:'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'Building and Pushing docker img to gcr.......'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}
                        
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                        gcloud config set project ${GCP_PROJECT}

                        gcloud auth configure-docker --quiet

                        docker build -t gcr.io/${GCP_PROJECT}/ete_diabetes:latest .

                        docker push gcr.io/${GCP_PROJECT}/ete_diabetes:latest
                        '''
                    }
                }
                
            }
        }
        stage('Deploy to Google Cloud Run'){
            steps{
                withCredentials([file(credentialsId: 'gcp-key' , variable : 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'Deploy to Google Cloud Run.............'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}


                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                        gcloud config set project ${GCP_PROJECT}

                        gcloud run deploy ml-project \
                            --image=gcr.io/${GCP_PROJECT}/ml-project:latest \
                            --platform=managed \
                            --region=us-central1 \
                            --allow-unauthenticated
                            
                        '''
                    }
                }
            }
        }
    }
}