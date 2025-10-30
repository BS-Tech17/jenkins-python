pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                // Pull latest code from your Git repository
                git branch: 'main', url: 'https://github.com/BS-Tech17/jenkins-python.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                // Install all required Python libraries
                sh '''
                echo "Installing Python dependencies..."
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Script') {
            steps {
                // Run your main Python script
                sh '''
                echo "Running Python script..."
                python main.py
                '''
            }
        }
    }

    post {
        success {
            echo 'Build completed successfully!'
        }
        failure {
            echo 'Build failed. Check console output for details.'
        }
    }
}
