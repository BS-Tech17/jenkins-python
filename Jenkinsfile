pipeline {
    agent any

    environment {
        PYTHON      = 'python3'
        VENV        = 'venv'
        FLASK_HOST  = '127.0.0.1'
        FLASK_PORT  = '8081'
    }

    options {
        timeout(time: 5, unit: 'MINUTES')
        timestamps()
    }

    stages {
        /* ---------- 1. Checkout ---------- */
        stage('Checkout') {
            steps {
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

        /* ---------- 2. Setup ---------- */
        stage('Setup') {
            steps {
                sh '''
                rm -rf $VENV
                $PYTHON -m venv $VENV
                source $VENV/bin/activate
                python -m pip install --upgrade pip
                pip install -r requirements.txt --quiet
                '''
            }
        }

        /* ---------- 3. Test ---------- */
        stage('Test') {
            steps {
                sh '''
                source $VENV/bin/activate
                mkdir -p reports
                pytest test_app.py \
                    -q \
                    --junitxml=reports/junit.xml \
                    --cov=main \
                    --cov-report=xml:reports/coverage.xml
                '''
            }
            post {
                always {
                    junit testResults: 'reports/junit.xml', allowEmptyResults: true
                    publishCoverage adapters: [cobertura('reports/coverage.xml')]
                }
            }
        }

        /* ---------- 4. Deploy ---------- */
        stage('Deploy') {
            when { branch 'main' }
            steps {
                sh '''
                source $VENV/bin/activate

                echo "=== KILL PORT $FLASK_PORT ==="
                fuser -k $FLASK_PORT/tcp || true

                echo "=== START FLASK ==="
                nohup python main.py > flask.log 2>&1 &

                sleep 4

                echo "=== HEALTH CHECK ==="
                curl -f http://$FLASK_HOST:$FLASK_PORT/health || exit 1

                echo
                echo "================================"
                echo "FLASK IS LIVE → http://localhost:8081"
                echo "================================"
                '''
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
        always  { cleanWs() }
    }
}
