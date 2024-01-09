pipeline {
    agent none 
    stages {
        stage('Test') {
            agent {
                docker {
                    image 'qnib/pytest'
                }
            }
            steps {
                sh 'pip install pytest_mock'
                sh 'py.test /var/jenkins_home/workspace/kantor5M_main/backend/src/backend/test.py'
            }
        }
        stage('Build') { 
            agent {
                docker {
                    image 'python:3.12.1-alpine3.19'
                    image 'node:20.10.0-alpine3.19'
                }
            }
            steps {
                sh '''
              cd /var/jenkins_home/workspace/kantor5M_main/backend
              './create_python_package.sh'
                ''' 
            }
        }
    }
}
