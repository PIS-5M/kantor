pipeline {
    agent none 
    stages {
        stage('Test') { 
            agent {
                docker {
                    image 'python:3.12.1-alpine3.19'
                    image 'qnib/pytest'
                }
            }
            steps {
                sh 'py.test /var/jenkins_home/workspace/kantor5M_main/backend/src/backend/test.py'
            }
        }
    }
}
