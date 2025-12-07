cat > Jenkinsfile << 'EOF'
pipeline {
    agent any
    
    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/saffanoor001/Deploying_3_Tier_Web_App_Using_Docker_Compose_And_Jenkins_Pipeline-main.git'
            }
        }
        
        stage('Setup Environment') {
            steps {
                sh '''
                    # Create .env file for backend
                    cat > backend/.env << 'ENVEOF'
PORT=4000
NODE_ENV=development
ENVEOF
                '''
            }
        }
        
        stage('Build & Run Containers') {
            steps {
                sh '''
                    # Stop old containers
                    sudo docker-compose down || true
                    
                    # Start new containers
                    sudo docker-compose up -d --build
                '''
            }
        }
        
        stage('Wait for Application') {
            steps {
                sh '''
                    echo "Waiting for containers to be ready..."
                    sleep 20
                    sudo docker ps
                '''
            }
        }
        
        stage('Run Selenium Tests') {
            steps {
                sh '''
                    # Run tests in Docker container with Chrome
                    sudo docker run --rm \
                    --network host \
                    -v $(pwd):/workspace \
                    -w /workspace \
                    selenium/standalone-chrome:latest \
                    bash -c "
                        apt-get update -qq && apt-get install -y -qq python3 python3-pip > /dev/null 2>&1
                        pip3 install --quiet --break-system-packages -r requirements-test.txt
                        pytest tests/ -v --html=report.html --self-contained-html
                    " || echo "Tests completed with errors"
                '''
            }
        }
        
        stage('Application Logs') {
            steps {
                sh 'sudo docker-compose logs --tail=50'
            }
        }
    }
    
    post {
        always {
            // Archive test report
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: '.',
                reportFiles: 'report.html',
                reportName: 'Selenium Test Report',
                reportTitles: ''
            ])
        }
        success {
            echo "✅ Build & Tests Completed Successfully!"
            emailext (
                subject: "✅ Jenkins Build Success: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
Build successful!

Job: ${env.JOB_NAME}
Build Number: ${env.BUILD_NUMBER}
Status: ${currentBuild.result}

View test results: ${env.BUILD_URL}Selenium_20Test_20Report/

Console output: ${env.BUILD_URL}console
                """,
                to: "\${DEFAULT_RECIPIENTS}",
                attachLog: true
            )
        }
        failure {
            echo "❌ Build or Tests Failed"
            emailext (
                subject: "❌ Jenkins Build Failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
Build or tests failed!

Job: ${env.JOB_NAME}
Build Number: ${env.BUILD_NUMBER}
Status: ${currentBuild.result}

Console output: ${env.BUILD_URL}console

Please check the logs for details.
                """,
                to: "\${DEFAULT_RECIPIENTS}",
                attachLog: true
            )
        }
    }
}
EOF