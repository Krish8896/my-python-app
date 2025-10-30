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
        stage('frontend and backend Test') { 
            steps {
                dir('frontend/frontends') { 
                    sh 'npm install' 
                    sh 'npm test -- --coverage' 
                }
                dir('backend') { 
                    sh 'docker-compose run --rm backend pytest --cov=. --cov-report=xml' 
                }
            }
        }
        stage('SonarQube Analysis') {
    steps {
        script {
            echo "Starting SonarQube analysis..."
            // Wrap SonarQube execution in a timeout to prevent infinite run
            timeout(time: 15, unit: 'MINUTES') {
                withSonarQubeEnv('sonarqube-server1') {
                    sh '''
                        # Clean old Sonar cache (optional safety)
                        rm -rf .scannerwork

                        # Run sonar-scanner with caching enabled
                        /var/lib/jenkins/tools/hudson.plugins.sonar.SonarRunnerInstallation/python-sonar-scanner1/bin/sonar-scanner \
                          -Dsonar.cache.enabled=true \
                          -Dsonar.log.level=INFO \
                          -Dsonar.verbose=false \
                          -X || true
                    '''
                }
            }
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
     /*   stage('Publish to Artifactory') {
            environment {
                ARTIFACTORY_URL = 'helloworlds.jfrog.io'
                ARTIFACTORY_REPO = 'docker-python-docker-local'
                ARTIFACTORY_CREDENTIALS = credentials('artifact-cred')
                IMAGE_NAME = 'python-app-backend'
                IMAGE_TAG = "python-flask"
            }
            steps {
                script {
                def ARTIFACTORY_IMAGE = "${ARTIFACTORY_URL}/${ARTIFACTORY_REPO}/${IMAGE_NAME}:${IMAGE_TAG}"
                sh """
                    echo ${ARTIFACTORY_CREDENTIALS_PSW} | docker login ${ARTIFACTORY_URL} -u ${ARTIFACTORY_CREDENTIALS_USR} --password-stdin
                    docker tag ${IMAGE_NAME}:latest ${ARTIFACTORY_IMAGE}
                    docker push ${ARTIFACTORY_IMAGE}
                """
                }
            }
            post {
                always {
                sh 'docker logout ${ARTIFACTORY_URL}'
                }
            }
        } */
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