pipeline {
    agent any

    environment {
        PYTHON = 'C:\\Users\\Teacher_Kabinet_7\\AppData\\Local\\Programs\\Python\\Python314\\python.exe'
    }

    stages {
        stage('Проверка Python') {
            steps {
                bat '"%PYTHON%" --version'
                bat '"%PYTHON%" -m pip --version'
            }
        }

        stage('Установка зависимостей') {
            steps {
                bat '"%PYTHON%" -m pip install -r requirements.txt'
            }
        }

        stage('Тестирование') {
            steps {
                bat '"%PYTHON%" -m pytest -v --junitxml=test-report.xml'
            }
        }

        stage('Сборка архива') {
            steps {
                bat '"%PYTHON%" -m zipfile -c shipping-module.zip shipping.py CHANGELOG.md'
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true,
                  testResults: 'test-report.xml'
        }

        success {
            archiveArtifacts artifacts: 'shipping-module.zip',
                             fingerprint: true
        }
    }
}