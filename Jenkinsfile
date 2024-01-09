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

    stage('Build') {
      agent {
        docker {
          image 'python:3.12.1-alpine3.19'
        }

      }
            steps {
                sh '''
              pwd ls -l
              cd /var/jenkins_home/workspace/kantor5M_main
              ls -a /var/jenkins_home/workspace/kantor5M_main
              pwd ls -l
              cd /var/jenkins_home/workspace/kantor5M_main/backend
              pwd ls -l
              chmod +x create_packages.sh
              pwd ls -l
              sh './create_packages.sh'
                ''' 
            }
    }

  }
}
