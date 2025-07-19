pipeline{
    agent any
    stages{
        stage('Clone Repository'){
            steps{
                script{
                    echo 'Cloning the repository...'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/n7kadda/ete_diabetes.git']])
                }
            }
        }
    }
}