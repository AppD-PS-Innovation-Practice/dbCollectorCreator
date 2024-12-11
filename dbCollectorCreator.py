# Script requires Requests Library 2.31.0 or later - https://requests.readthedocs.io/en/latest/
import argparse
import json
import logging
import requests
import subprocess
import sys



def getAccessToken(account, client_name, client_secret):
    logging.info('Getting Access Token')
    response = requests.post(f"https://{account}.saas.appdynamics.com/controller/api/oauth/access_token",
                             headers={'Content-Type': 'application/x-www-form-urlencoded'},
                             data={'grant_type': 'client_credentials', 'client_id': f"{client_name}@{account}", 'client_secret': client_secret})
    logging.info(f"response = {response}")
    access_token = response.json()['access_token']
    logging.info(f"access_token = {access_token}")
    logging.info('===========')
    return access_token

def main(loglevel,
         db_collector_data_filename,
         controller_account, appd_clientname, appd_clientsecret):
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(message)s\n", level=loglevel)
    appd_url = f'https://{controller_account}.saas.appdynamics.com/controller/rest/databases/collectors/create'
    headers = {'Accept': 'application/json',
               'Content-Type': 'application/json'}

    account = controller_account
    client_name = appd_clientname
    client_secret = appd_clientsecret
    access_token = ''
    db_collector_data = []
    db_collector_list = []
    try:
        with open(db_collector_data_filename, "r") as db_collector_data_file:
            db_collector_data = db_collector_data_file.read().splitlines()
            logging.info(f'db_collector_data:\n{db_collector_data}')
        for db_collector in db_collector_data:
            db_type = db_collector.split(",")[0]
            db_agent_name = db_collector.split(",")[1]
            db_collector_name = db_collector.split(",")[2]
            db_hostname = db_collector.split(",")[3]
            db_port = db_collector.split(",")[4]
            db_user = db_collector.split(",")[5]
            db_pswd = db_collector.split(",")[6]

            logging.info(f'db_type is {db_type}, db_agent_name is {db_agent_name}, '
                         f'db_hostname is {db_hostname}, db_port is {db_port}, db_user is {db_user}, db_pswd is {db_pswd}')

            dbcollector_payload = json.dumps(
                {
                    "type": db_type,
                    "agentName": db_agent_name,
                    "name": db_collector_name,
					"hostname": db_hostname,
					"port": db_port,
					"username": db_user,
                    "password": db_pswd
                }
                )

            logging.info(f'going to add post dbcollector_payload: {dbcollector_payload}')
            db_collector_list.append(dbcollector_payload)

    except Exception as error:
        logging.error(f'An exception occurred: {error}')
            # logging.error(f'Unable to open {db_collector_data_filename}')

    with requests.Session() as session:

        access_token = getAccessToken(account, client_name, client_secret)
        session.headers = headers = {'Authorization': f"Bearer {access_token}",
									'Accept': 'application/json',
									'Content-Type': 'application/json'}

        for data in db_collector_list:
            try:
                logging.info(f'session.headers is {session.headers}')
                logging.info(f'appd_url is {appd_url}')
                logging.info(f'JSON Payload is {data}')
                response = session.post(appd_url, data=data)
                logging.info(
                    f'POST Status Code: {response.status_code} POST Response: {response.text}')
                # Status code will be 204 as listener responds with no_content
                # add 200
                if response.status_code != 204 and response.status_code != 200:
                    logging.error(
                        f'Expected 204 or 200. Got {response.status_code} for status code')
            except requests.exceptions.RequestException as exc:
                logging.error(
                    f'POST failed for {appd_url} with dbcollector_payload {data}\n{exc}')
                sys.exit(1)


"""
COMMENTS
"""

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('loglevel',
                        help='Logging level - mainly for debugging',
                        nargs='?',
                        default='ERROR', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
    parser.add_argument('db_collector_data_filename',
                        help='Data file of list of db collector details',
                        nargs='?',
                        default='/appd/extensions/db_collector_data.csv')
    parser.add_argument('controller_account',
                        help='controller_account',
                        nargs='?', default='controller_account')
    parser.add_argument('appd_clientname',
                        help='appd_clientname',
                        nargs='?', default='appd_clientname')
    parser.add_argument('appd_clientsecret',
                        help='appd_clientsecret',
                        nargs='?', default='appd_clientsecret')
    args = parser.parse_args()
    # print(args)

    main(args.loglevel,
         args.db_collector_data_filename,
         args.controller_account,
		 args.appd_clientname, args.appd_clientsecret)
