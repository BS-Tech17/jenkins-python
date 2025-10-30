pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/BS-Tech17/jenkins-python.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                echo Installing dependencies...
                python -m pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Script') {
            steps {
                bat '''
                echo Running Python script...
                python main.py
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Build completed successfully!'
        }
        failure {
            echo '❌ Build failed. Check console output for details.'
        }
    }
}
