
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies and Test') {
            steps {
                sh 'python3 --version'
                sh 'python3 -m venv .venv'
                sh '.venv/bin/pip install -r requirements.txt'
                sh '.venv/bin/python -m pytest -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t taskflow-app .'
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl --kubeconfig=/var/jenkins_home/.kube/config apply -f deployment.yaml'
                sh 'kubectl --kubeconfig=/var/jenkins_home/.kube/config apply -f service.yaml'
                sh 'kubectl --kubeconfig=/var/jenkins_home/.kube/config rollout status deployment/taskflow --timeout=120s'
            }
        }
    }
}
