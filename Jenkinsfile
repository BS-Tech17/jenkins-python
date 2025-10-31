pipeline {
    agent any

    environment {
        PYTHON = 'python3'
        VENV = 'venv'
        FLASK_HOST = '127.0.0.1'
        FLASK_PORT = '8081'
    }

    options {
        timeout(time: 5, unit: 'MINUTES')
        timestamps()
    }

    stages {
        stage('Checkout') {
            steps {
                timeout(time: 30, unit: 'SECONDS') {
                    checkout scmGit(
                        branches: [[name: '*/main']],
                        userRemoteConfigs: [[url: 'https://github.com/stardxst12/jenkins-python.git']],
                        extensions: [
                            [$class: 'CloneOption', shallow: true, depth: 1, noTags: true],
                            [$class: 'CleanCheckout']
                        ]
                    )
                }
            }
        }

        stage('Setup') {
            steps {
                timeout(time: 90, unit: 'SECONDS') {
                    sh '''
                    rm -rf $VENV
                    $PYTHON -m venv $VENV
                    . $VENV/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt --quiet
                    '''
                }
            }
        }

        stage('Test') {
            steps {
                timeout(time: 45, unit: 'SECONDS') {
                    sh '''
                    . $VENV/bin/activate
                    mkdir -p reports
                    pytest tests/ \
                        -q \
                        --junitxml=reports/junit.xml \
                        --cov=main \
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

        stage('Deploy') {
            when { branch 'main' }
            steps {
                timeout(time: 30, unit: 'SECONDS') {
                    sh '''
                    . $VENV/bin/activate

                    echo "=== KILL PORT $FLASK_PORT ==="
                    fuser -k $FLASK_PORT/tcp || true

                    echo "=== START FLASK ==="
                    nohup python3 main.py > flask.log 2>&1 &

                    sleep 4

                    echo "=== HEALTH CHECK ==="
                    curl -f http://$FLASK_HOST:$FLASK_PORT/health || exit 1

                    echo "================================"
                    echo "  FLASK IS LIVE: http://localhost:$FLASK_PORT"
                    echo "================================"
                    '''
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: '*.log', allowEmptyArchive: true
                }
            }
        }
    }

    post {
        success { echo "SUCCESS – http://localhost:8081" }
        failure { echo "FAILED – see console" }
        always { cleanWs() }
    }
}
