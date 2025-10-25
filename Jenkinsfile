pipeline {
    agent any
    environment {
        DOCKER_COMPOSE_DIR = "${WORKSPACE}" // adjust if your compose file is in a subdir
    }
    stages {
        stage('Build') {
            steps {
                dir("${DOCKER_COMPOSE_DIR}") {
                    sh 'docker-compose build'
                }
            }
        }
        stage('Test') {
            steps {
                dir("${DOCKER_COMPOSE_DIR}/backend") {
                    sh 'docker-compose up -d db'
                    // Wait for DB to be healthy instead of static sleep
                    sh '''
                        echo "Waiting for MySQL to be healthy..."
                        for i in {1..30}; do
                          if [ "$(docker inspect -f {{.State.Health.Status}} my-python-app-db-1)" = "healthy" ]; then
                            echo "MySQL is healthy!"
                            break
                          fi
                          sleep 2
                        done
                    '''
                    sh 'docker-compose run --rm backend python -m unittest discover'
                    sh 'docker-compose down'
                }
            }
        }
        stage('SonarQube Analysis') {
            environment {
                scannerHome = tool 'python-sonar-scanner1'
            }
                steps {
                        withSonarQubeEnv('sonarqube-server1') {
                        sh "${scannerHome}/bin/sonar-scanner"
                    }
                }
        }
        stage("Quality Gate"){
            steps {
                script {
            timeout(time: 15, unit: 'MINUTES') { // Just in case something goes wrong, pipeline will be killed after a timeout
            def qg = waitForQualityGate() // Reuse taskId previously collected by withSonarQubeEnv
            if (qg.status != 'OK') {
            error "Pipeline aborted due to quality gate failure: ${qg.status}"
            }
            }
        }
            }
        }
        stage('Deploy') {
            steps {
                dir("${DOCKER_COMPOSE_DIR}") {
                    sh 'docker-compose up -d'
                }
                echo 'Deployment complete.'
            }
        }
    }
    post {
        always {
            echo 'Pipeline finished.'
        }
        success {
            echo 'Pipeline completed successfully.'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}