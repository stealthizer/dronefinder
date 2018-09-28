node {
    def app

    stage('Clone repository') {
        /* Ensure we can clone the repository */
        checkout scm
    }

    stage('Build image') {
        /* This builds the actual image; synonymous to
         * docker build on the command line */
        app = docker.build("stealthizer/dronefinder")
    }

    stage('Test image') {
            /* No real tests so it just passes this step always OK */
            sh 'echo "Tests passed"'
    }

    stage('Push image') {
        /* Finally, we'll push the image with two tags:
         * First, a short hash that identifies the commit in git
         * Second, the 'latest' tag.
         * Pushing multiple tags is cheap, as all the layers are reused. */
         sh "git rev-parse --short HEAD > .git/commit-id"
         def commit_id = readFile('.git/commit-id').trim()
         docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials') {
            app.push("${commit_id}")
            app.push("latest")
        }
    }
}
