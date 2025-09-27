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
                // Example: run backend tests
                dir("${DOCKER_COMPOSE_DIR}/backend") {
                    sh 'docker-compose up -d db'
                    sh 'sleep 10' // wait for DB to be ready
                    sh 'docker-compose run --rm backend python -m unittest discover'
                    sh 'docker-compose down'
                }
            }
        }
        stage('SonarQube Analysis') {
            environment {
                scannerHome = tool 'python-sonar-scanner'
            }
                steps {
                        withSonarQubeEnv('sonarqube-server') {
                        sh "${scannerHome}/bin/sonar-scanner"
                    }
                }
        }
        stage("Quality Gate"){
            steps {
                script {
            timeout(time: 15, unit: 'MINUTES') { // Just in case something goes wrong, pipeline will be killed after a timeout
            qg = waitForQualityGate() // Reuse taskId previously collected by withSonarQubeEnv
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