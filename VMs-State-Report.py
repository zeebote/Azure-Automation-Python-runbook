"""
Azure Automation documentation : https://aka.ms/azure-automation-python-documentation
Azure Python SDK documentation : https://aka.ms/azure-python-sdk
"""
import sys
import pprint
import automationassets
from azure.mgmt.compute import ComputeManagementClient
import sendgrid
from sendgrid.helpers.mail import *
SENDGRID_APIKEY = 'This should be your SendGrid API key'

def _send_report(sub, cont, to_e):
    # SendGrid now require sender verification - this from email must be verified by your SendGrid account 
    from_email = Email("aa-report@yourdomain.com")
    to_email = to_e
    subject = sub
    content = cont
    mail = Mail(from_email, to_email, subject, content)
    sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_APIKEY)
    response = sg.send(mail)
    return response

def get_automation_runas_credential(runas_connection):
    """ Returns credentials to authenticate against Azure resource manager """
    from OpenSSL import crypto
    from msrestazure import azure_active_directory
    import adal

    # Get the Azure Automation RunAs service principal certificate
    cert = automationassets.get_automation_certificate("AzureRunAsCertificate")
    pks12_cert = crypto.load_pkcs12(cert)
    pem_pkey = crypto.dump_privatekey(crypto.FILETYPE_PEM, pks12_cert.get_privatekey())

    # Get run as connection information for the Azure Automation service principal
    application_id = runas_connection["ApplicationId"]
    thumbprint = runas_connection["CertificateThumbprint"]
    tenant_id = runas_connection["TenantId"]

    # Authenticate with service principal certificate
    resource = "https://management.core.windows.net/"
    authority_url = ("https://login.microsoftonline.com/" + tenant_id)
    context = adal.AuthenticationContext(authority_url)
    return azure_active_directory.AdalAuthentication(
        lambda: context.acquire_token_with_client_certificate(
            resource,
            application_id,
            pem_pkey,
            thumbprint)
    )


# Authenticate to Azure using the Azure Automation RunAs service principal
runas_connection = automationassets.get_automation_connection("AzureRunAsConnection")
azure_credential = get_automation_runas_credential(runas_connection)

# Initilize computer management
compute_client = ComputeManagementClient(
    azure_credential,
    str(runas_connection["SubscriptionId"])
)

# Get list of all VMs and print them out
vm_list = compute_client.virtual_machines.list_all()
# You can also get VMs on specific resource group by commend out above line and uncomment the next line 
# and replace resource_group with your resource
#vm_list = compute_client.virtual_machines.list(resource_group_name=resource_group)
i = 0
a = 0
body = ""
for vm in vm_list:
    # Get resource group 
    array = vm.id.split("/")
    resource_group = array[4]
    # Assign variable
    vm_name = vm.name
    vm_location = vm.location
    vm_state = compute_client.virtual_machines.get(resource_group, vm_name, expand='instanceView')
    vm_opers = vm_state.storage_profile.os_disk.os_type.value
    # Get VM status
    stat = vm_state.instance_view.statuses
    status = len(stat) >= 2 and stat[1]
    display = status.display_status
    #  count number of running VM
    if(display == 'VM running'):
        body += '  Name: ' + vm_name + '\n'
        body += '  OS: ' + vm_opers + '\n'
        body += '  Location: ' + vm_location + '\n'
        body += '  Status: ' + display + '\n'
        a = a + 1
    else:
        body += '  Name: ' + vm_name + '\n'
        body += '  OS: ' + vm_opers + '\n'
        body += '  Location: ' + vm_location + '\n'
        body += '  Status: ' + display + '\n'
    body += '-----------------------------\n'
    i = i + 1
# Email info
subject = 'There are total ' + str(i) + ' virtual machines, in which have ' + str(a) + ' running'
to_email = To("youraddress@yourdomain.com")
content = Content("text/plain", body)
_send_report(subject, content, to_email)
