pipeline {
    agent any

    environment {
        PYTHON      = 'python'          // or 'python3'
        VENV        = 'venv'
        FLASK_HOST  = '127.0.0.1'
        FLASK_PORT  = '8081'            // same port you want
    }

    options {
        timeout(time: 5, unit: 'MINUTES')
        timestamps()
    }

    stages {
        /* -------------------------------------------------
           1. Checkout – shallow + 30‑second timeout
           ------------------------------------------------- */
        stage('Checkout') {
            steps {
                timeout(time: 30, unit: 'SECONDS') {
                    checkout scmGit(
                        branches: [[name: '*/main']],
                        userRemoteConfigs: [[url: 'https://github.com/BS-Tech17/jenkins-python.git']],
                        extensions: [
                            [$class: 'CloneOption', shallow: true, depth: 1, noTags: true],
                            [$class: 'CleanCheckout']
                        ]
                    )
                }
            }
        }

        /* -------------------------------------------------
           2. Setup – venv + deps (cached pip)
           ------------------------------------------------- */
        stage('Setup') {
            steps {
                timeout(time: 90, unit: 'SECONDS') {
                    bat '''
                    if exist %VENV% rmdir /s /q %VENV%
                    %PYTHON% -m venv %VENV%
                    call %VENV%\\Scripts\\activate
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt --quiet
                    '''
                }
            }
        }

        /* -------------------------------------------------
           3. Test – JUnit + Cobertura only (no HTML)
           ------------------------------------------------- */
        stage('Test') {
            steps {
                timeout(time: 45, unit: 'SECONDS') {
                    bat '''
                    call %VENV%\\Scripts\\activate
                    mkdir reports 2>nul
                    pytest test_app.py ^
                        -q ^
                        --junitxml=reports/junit.xml ^
                        --cov=main ^
                        --cov-report=xml:reports/coverage.xml
                    '''
                }
            }
            post {
                always {
                    junit testResults: 'reports/junit.xml', allowEmptyResults: true
                    publishCoverage adapters: [cobertura('reports/coverage.xml')]
                }
            }
        }

        /* -------------------------------------------------
           4. Deploy – kill port → start Flask → quick health
           ------------------------------------------------- */
        stage('Deploy') {
            when { branch 'main' }
            steps {
                timeout(time: 30, unit: 'SECONDS') {
                    bat '''
                    call %VENV%\\Scripts\\activate

                    echo === KILL PORT %FLASK_PORT% ===
                    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :%FLASK_PORT%') do taskkill /PID %%a /F >nul 2>&1

                    echo === START FLASK ===
                    start "" /b python main.py

                    timeout /t 4 >nul

                    echo === HEALTH CHECK ===
                    curl -f http://%FLASK_HOST%:%FLASK_PORT%/health || exit 1

                    echo.
                    echo ================================================
                    echo    FLASK IS LIVE → http://localhost:8081
                    echo ================================================
                    '''
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: '*.log,port_check.txt', allowEmptyArchive: true
                }
            }
        }
    }

    post {
        success { echo "SUCCESS – http://localhost:8081" }
        failure { echo "FAILED – see console" }
        always  { cleanWs() }
    }
}
