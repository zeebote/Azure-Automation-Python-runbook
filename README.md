# Azure-Automation-Python-Runbook
If you are responsible for an Azure subcription then you should know how many VMs are running, especially when the subcription have been access by different groups such as Engineering, Marketing, Sales... <br>
This Python runbook will count all VMs in Azure subcription and can email the report by schedule so you can roughtly know how your Azure resources has been ultilized and won't supprise when recieve the monthly bill. 
<br>

**Requirements:**
1. Azure Automation Account - Follow this [link](https://docs.microsoft.com/en-us/azure/automation/automation-create-standalone-account) for instruction to create Automation Account
1. SendGrid Python package - This script using SendGrid to send email, Azure subscription can have a free SendGrid account with limit at 25,000 messages a day. Please follow this [link](https://docs.microsoft.com/en-us/azure/automation/python-packages) for instruction to import a Python package to Azure Automation account.
1. SendGrid API key - Please follow this [link](https://docs.microsoft.com/en-us/azure/sendgrid-dotnet-how-to-send-email#next-steps) for instruction how to create an Azure SendGrid account and get API key
<br>

**How to use:**
1. Create a Azure Python runbook - Follow this [link](https://docs.microsoft.com/en-us/azure/automation/learn/automation-tutorial-runbook-textual-python2) for instruction to create Python run book and copy and paste the content of the VM-State-Report.py in to the run book textual editor. You also can import this script to Azure run book by click on **Import a runbook**
2. Create a schedule in Azure Automation account then link the new runbook to this schedule.   
