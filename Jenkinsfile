#!/usr/bin/env groovy

podTemplate(label: 'aws-stash', containers: [
    containerTemplate(name: 'python', image: 'python:3.6', command: 'cat', ttyEnabled: true),
    containerTemplate(name: 'docker', image: 'docker', command: 'cat', ttyEnabled: true)
  ],
  volumes: [
    hostPathVolume(mountPath: '/var/run/docker.sock', hostPath: '/var/run/docker.sock'),
  ]
  ) {

    node('aws-stash') {

        def myRepo = checkout scm
        def gitCommit = myRepo.GIT_COMMIT
        def gitBranch = myRepo.GIT_BRANCH
        def shortGitCommit = "${gitCommit[0..6]}"
        def dockerNamespace = "askainet"
        def dockerImage = "aws-stash"

        stage('Python test') {
            container('python') {
                sh """
                    pip install -r requirements.txt
                    pytest -v
                """
            }
        }

        stage('Python build') {
            container('python') {
                sh "pip install --install-option='--prefix=/install' ."
            }
        }

        stage('Docker image') {
            container('docker') {
                withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'DOCKER_HUB_USER', passwordVariable: 'DOCKER_HUB_PASSWORD')]) {
                    sh 'docker login -u ${DOCKER_HUB_USER} -p ${DOCKER_HUB_PASSWORD}'
                    sh """
                        docker pull ${dockerNamespace}/${dockerImage} || true
                        docker build --cache-from=${dockerNamespace}/${dockerImage} -t ${dockerNamespace}/${dockerImage}:${shortGitCommit} .
                        docker push ${dockerNamespace}/${dockerImage}:${shortGitCommit}
                    """
                }
            }
        }

    }

}
