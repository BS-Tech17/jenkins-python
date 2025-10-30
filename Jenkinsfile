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
                sh '''
                python -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                . venv/bin/activate
                pytest -v
                '''
            }
        }

        stage('Code Quality (Optional)') {
            steps {
                sh '''
                . venv/bin/activate
                pylint app.py || true
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                echo "Starting Flask app..."
                . venv/bin/activate
                nohup python app.py &
                '''
            }
        }
    }
}
