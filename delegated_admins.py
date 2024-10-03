import boto3
from botocore.exceptions import ClientError

org_client = boto3.client('organizations')

# Get enabled services
enabled_services_response = org_client.list_aws_service_access_for_organization()

# Get delegated administrators for each service
for enabled_service in enabled_services_response['EnabledServicePrincipals']:
    service_principal = enabled_service['ServicePrincipal']

    try:
        delegated_admins_output = org_client.list_delegated_administrators(ServicePrincipal=service_principal)
        if delegated_admins_output['DelegatedAdministrators']:
            admin = delegated_admins_output['DelegatedAdministrators'][0]
            print(f"Service: {service_principal}, Delegated Administrator: {admin['Name']} (ID: {admin['Id']})")
        else:
            print(f"Service: {service_principal}, Delegated Administrator: None")
    except ClientError as e:
        if e.response['Error']['Code'] == 'InvalidInputException':
            print(f"Service: {service_principal}, Error: Unrecognized service principal")
        else:
            raise e  # Re-raise other exceptions
