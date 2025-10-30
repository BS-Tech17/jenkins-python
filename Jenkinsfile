pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/BS-Tech17/jenkins-python.git'
            }
        }

        stage('Setup Environment') {
            steps {
                bat '''
                python -m venv venv
                call venv\\Scripts\\activate
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                call venv\\Scripts\\activate
                pytest -v
                '''
            }
        }

        stage('Code Quality (Optional)') {
            steps {
                bat '''
                call venv\\Scripts\\activate
                pylint app.py || exit 0
                '''
            }
        }

        stage('Deploy') {
            steps {
                bat '''
                echo Starting Flask app...
                call venv\\Scripts\\activate
                python app.py
                '''
            }
        }
    }
}
