Group 1 Members:
Andrew
Enrique
Ruby

Preparation:
1) Must have Flask-bcrypt installed:
easy_install --user flask-bcrypt
or
pip install --user flask-bcrypt

2) Must have Flask-BasicAuth installed:
easy_install --user Flask-BasicAuth
or
pip install --user Flask-BasicAuth

Runnng the microservices:
Enter the command "foreman start"
This will execute the Procfile

Running Tavern for test:
Enter the command "pytest"
This will find all tavern.yaml files
The test will only run successfully when the microservices are running

Port numbers:
The port numbers for each microservices is as follows:
	articleP: 5100
        tagP: 5300
        commentP: 5000
        userP: 5200
If the microservices are running on different ports, edit the "includes.yaml" file
 and these values to the port number your flask is running them in


