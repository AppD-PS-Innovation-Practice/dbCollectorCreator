How to run:


Basic authentication version:
python ./dbCollectorCreator.py DEBUG "PATH\TO\db_collector_data.csv" YOUR_COMPANY.saas.appdynamics.com YOUR_ACCOUNT@YOUR_COMPANY YOURPASSWORD


API client version:
python ./dbCollectorCreator.py DEBUG "PATH\TO\db_collector_data.csv" YOUR_COMPANY api-client-name api-client-secret

To create the api-client:
1 Login to the controller with Administrator access
2 Depending on controller version
  -- Click on the gear in the top right corner
  or
  -- Click on your name in the top right corner
3 Select the Administration menu item
4 Select the API Clients menu
5 Click on the Create button
6 Enter a Client Name
7 Add the DB Monitoring Administrator role
8 Generate Secret
9 Copy this value



CSV input data file format:
	db_type, db_agent_name, db_collector_name, db_hostname, db_port, db_user, db_pswd
ex:
	POSTGRESQL,DatabaseAgent_ABC123,DatabaseCollector_ABC123,192.168.0.1,5432,admin,abc123

API details:
https://docs.appdynamics.com/appd/23.x/latest/en/extend-appdynamics/appdynamics-apis/database-visibility-api
