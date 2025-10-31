pipeline {
    agent any

    environment {
        PYTHON      = 'python'          // use 'python3' if needed
        VENV        = 'venv'
        FLASK_HOST  = '127.0.0.1'
        FLASK_PORT  = '8081'            // same port as Jenkins UI
    }

    options {
        timeout(time: 15, unit: 'MINUTES')
        timestamps()
    }

    stages {
        stage('Network Check') {
            steps {
                bat '''
                nslookup github.com
                ping -n 2 github.com
                '''
            }
        }

        stage('Checkout') {
            steps {
                retry(3) {
                    checkout scmGit(
                        branches: [[name: '*/main']],
                        userRemoteConfigs: [[url: 'https://github.com/BS-Tech17/jenkins-python.git']]
                    )
                }
            }
        }

        stage('Setup') {
            steps {
                bat '''
                if exist %VENV% rmdir /s /q %VENV%
                %PYTHON% -m venv %VENV%
                call %VENV%\\Scripts\\activate
                python -m pip install --upgrade pip
                pip install -r requirements.txt
                pip list
                '''
            }
        }

        stage('Test') {
            steps {
                bat '''
                call %VENV%\\Scripts\\activate
                mkdir reports 2>nul
                pytest test_app.py -v ^
                    --junitxml=reports/junit.xml ^
                    --cov=main ^
                    --cov-report=xml:reports/coverage.xml ^
                    --cov-report=html:reports/html-cov
                '''
            }
            post {
                always {
                    junit 'reports/junit.xml'
                    publishCoverage adapters: [cobertura('reports/coverage.xml')]
                    archiveArtifacts artifacts: 'reports/html-cov/**', allowEmptyArchive: true
                }
            }
        }

        stage('Deploy to 8081') {
            when { branch 'main' }
            steps {
                bat '''
                call %VENV%\\Scripts\\activate

                echo === KILL ANY PROCESS ON PORT %FLASK_PORT% ===
                netstat -ano | findstr :%FLASK_PORT% > port_check.txt
                if not errorlevel 1 (
                    for /f "tokens=5" %%a in (port_check.txt) do (
                        taskkill /PID %%a /F
                        echo Killed PID %%a
                    )
                ) else (
                    echo No process on port %FLASK_PORT%
                )

                echo === START FLASK ON %FLASK_HOST%:%FLASK_PORT% ===
                start "" /b python main.py

                timeout /t 6 >nul

                echo === HEALTH CHECK ===
                curl -f http://%FLASK_HOST%:%FLASK_PORT%/health || exit 1

                echo.
                echo ================================================
                echo    FLASK APP IS NOW LIVE!
                echo    Visit: http://localhost:8081
                echo ================================================
                '''
            }
            post {
                always {
                    // Fixed: Named argument 'artifacts'
                    archiveArtifacts artifacts: '*.log,port_check.txt', allowEmptyArchive: true
                }
            }
        }
    }

    post {
        success {
            echo "SUCCESS! Open http://localhost:8081"
        }
        failure {
            echo "FAILED! Check logs above."
        }
        always {
            cleanWs()
        }
    }
}
