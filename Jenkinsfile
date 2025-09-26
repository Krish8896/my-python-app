pipeline {
    agent any
    environment {
        DOCKER_COMPOSE_DIR = "${WORKSPACE}" // adjust if your compose file is in a subdir
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/your-org/your-repo.git'
            }
        }
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
