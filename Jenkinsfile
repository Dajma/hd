pipeline {
   agent any
   

   
   stages {
		   stage('Remove old versions of charts') {
                steps {
					  sh "cleanup-charts.py"

				}
			}   
			
	}
}
