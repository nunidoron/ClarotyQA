pipeline {
    agent any

    options {
        timestamps()
    }

    environment {
        BASE_URL = 'https://demo.xsa.claroty.com'
        HEADLESS = 'true'
        BROWSER_EXECUTABLE_PATH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        LOGIN_USERNAME = credentials('claroty-login-username')
        LOGIN_PASSWORD = credentials('claroty-login-password')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Set Up Python') {
            steps {
                sh 'python3 -m venv .venv'
                sh '.venv/bin/python -m pip install --upgrade pip'
                sh '.venv/bin/python -m pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh '.venv/bin/python -m pytest'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'artifacts/**/*', allowEmptyArchive: true
            junit testResults: 'artifacts/reports/*.xml', allowEmptyResults: true
        }
    }
}
