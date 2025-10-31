pipeline {
    agent any

    environment {
        PYTHON = 'python'  // Use 'python3' if needed
        VENV = 'venv'
        APP_MODULE = 'main:app'  // main.py + app = Flask(__name__)
    }

    options {
        timeout(time: 15, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
        retry(1)  // Retry entire pipeline on transient failure
    }

    stages {
        stage('Network Diagnostics') {
            steps {
                bat '''
                echo === DNS Resolution Test ===
                nslookup github.com
                echo.
                echo === Ping Test ===
                ping -n 4 github.com
                echo.
                echo === Git Remote Test ===
                git ls-remote https://github.com/BS-Tech17/jenkins-python.git
                echo.
                echo === Proxy Settings ===
                echo HTTP_PROXY=%HTTP_PROXY%
                echo HTTPS_PROXY=%HTTPS_PROXY%
                '''
            }
        }

        stage('Checkout Code') {
            steps {
                script {
                    retry(3) {
                        timeout(time: 2, unit: 'MINUTES') {
                            checkout scmGit(
                                branches: [[name: '*/main']],
                                userRemoteConfigs: [[
                                    url: 'https://github.com/BS-Tech17/jenkins-python.git'
                                ]],
                                extensions: [
                                    [$class: 'CloneOption', shallow: true, depth: 1, noTags: false],
                                    [$class: 'CleanCheckout']
                                ]
                            )
                        }
                        sleep 2
                    }
                }
                bat '''
                echo === Workspace Contents ===
                dir
                echo.
                echo === Recent Commits ===
                git log --oneline -5
                '''
            }
        }

        stage('Setup Environment') {
            steps {
                bat '''
                echo === Creating Virtual Environment ===
                if exist %VENV% rmdir /s /q %VENV%
                %PYTHON% -m venv %VENV%
                call %VENV%\\Scripts\\activate
                python -m pip install --upgrade pip
                if exist requirements.txt (
                    pip install -r requirements.txt
                    echo Installed dependencies
                ) else (
                    echo WARNING: requirements.txt not found!
                )
                pip list
                '''
            }
        }

        stage('Run Tests') {
            steps {
                bat '''
                call %VENV%\\Scripts\\activate
                mkdir reports 2>nul
                pytest test_app.py ^
                    -v ^
                    --junitxml=reports/junit.xml ^
                    --cov=main ^
                    --cov-report=xml:reports/coverage.xml ^
                    --cov-report=html:reports/html-cov ^
                    --cov-report=term-missing
                '''
            }
            post {
                always {
                    junit testResults: 'reports/junit.xml', allowEmptyResults: true
                    publishCoverage adapters: [cobertura('reports/coverage.xml')]
                    archiveArtifacts artifacts: 'reports/html-cov/**', allowEmptyArchive: true
                }
            }
        }

        stage('Code Quality') {
            steps {
                bat '''
                call %VENV%\\Scripts\\activate
                pylint main.py --exit-zero --output-format=json:pylint-report.json
                '''
            }
            post {
                always {
                    recordIssues enabledForFailure: true, tool: pyLint(pattern: 'pylint-report.json')
                }
            }
        }

        stage('Deploy') {
            when { branch 'main' }
            steps {
                bat '''
                call %VENV%\\Scripts\\activate
                echo === Stopping any running app ===
                taskkill /f /im python.exe 2>nul || echo No Python process to kill
                taskkill /f /im gunicorn.exe 2>nul || echo No Gunicorn process to kill

                echo === Starting Flask App ===
                start "" /b python main.py

                echo === Waiting for app to start ===
                timeout /t 5 >nul

                echo === Health Check ===
                curl -f http://localhost:5000/health || exit 1
                echo App is LIVE at http://localhost:5000
                '''
            }
            post {
                always {
                    archiveArtifacts artifacts: '*.log,access.log,error.log', allowEmptyArchive: true
                }
            }
        }
    }

    post {
        always {
            echo "=== Build Finished ==="
            cleanWs()
        }
        success {
            echo "Pipeline SUCCEEDED!"
        }
        failure {
            echo "Pipeline FAILED - Check logs above"
        }
    }
}
