pipeline {
    agent none 
    stages {
        stage('Test') { 
            agent {
                    dockerfile true
            }
            steps {
                sh 'py.test /var/jenkins_home/workspace/kantor5M_main/backend/src/backend/test.py'
            }
        }
    }
}
