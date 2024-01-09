pipeline {
    agent none 
    stages {
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
              sh './create_python_package.sh'
                ''' 
            }
        }
    }
}
