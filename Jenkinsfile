pipeline{
    agent any

    environment{
        VENV_DIR = 'venv'
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
    }
}