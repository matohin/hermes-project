# Hermes Project

## Why?

Hermes project first prototype - connecting resources from personal Microsof account (Miscrosoft Graph) with Telegram bot.

Core technologies:

- Azure Functions
- Azure Service Bus
- Azure Key Vult
- Application Insights
- Python / pipenv / pytest
- MSAL

Just for fun/learning purposes, but real/working solution.

## How to deploy

## Resources on Azure / AzureDevops

1. Create a resource group for Dev environment. `New-AzResourceGroup -Name hermes-proj-dev -Location '<Azure region>'`
2. Create a DevOps service connection for deploy to RG
3. Create pipeline pointing to `pipeline_dev.yml`
4. Give permissions to pipeline (section below)
5. Fill / ceck RG/Subscription/Service connaction variables in `pipeline_dev.yml`
6. Deploy
7. Fill in secrets to created Key Vault and deploy again
8. Repeat for Prod / `pipeline_prod.yml`

### Give pipeline premissions to deploy role assignment

This project uses RBAC permissions model and creates role assignment to give function app managed identity acces to azure deviops. Azure DevOps service connection identity should be given a pemission to create role assignment in the group, if pipeline is used to create a role assignment. Alternatives are: create role assignment manually on the portal and take it out of the template or use KeyVault access policy and disable RBAC permissions on KeyVault.

Find Azure DevOps service principle:

``` Powershell
$PiplineServicePrincipal = Get-AzADServicePrincipal -ApplicationId <application ID of connection SP> # in connection settings
$PermanentInfrastructureResourceGroup = Get-AzResourceGroup -Name <resource group name>
```

Assign a role:

``` Powershell
New-AzRoleAssignment -ObjectId $PiplineServicePrincipal.Id -RoleDefinitionId (Get-AzRoleDefinition -Name "User Access Administrator").Id -Scope $PermanentInfrastructureResourceGroup.ResourceId
```

Connection identity also uses secrets at trploy time, so it will need a respective role.

``` Powershell
New-AzRoleAssignment -ObjectId $PiplineServicePrincipal.Id -RoleDefinitionId (Get-AzRoleDefinition -Name "Key Vault Secrets User").Id -Scope $PermanentInfrastructureResourceGroup.ResourceId
```

## Adding secrets to the KeyVault

``` Powershell
$vaultName = 'kv-hermes-proj'
Set-AzKeyVaultSecret -VaultName $vaultName -SecretName "secretName" -SecretValue (ConvertTo-SecureString -String 'secretValuexxxyyyzzz' -AsPlainText -Force)
```

## Role assignment re-creation

Every time Function App is deleted, "Key Vault Secrets Officer" role assignment on resource group for system managed identity of the app should be removed manually to avoid conflict on new role assignment.

*TODO*: Switch to user assigned Function App identity to mitigate this issue.

## Just useful Commands

pipenv lock -r > .\requirements.txt

``` Powershell
gc .\.gitignore > .\.funcignore

Get-AzRoleDefinition | Where-Object{$_.name -like "*search_for_roles*"}

New-AzRoleAssignment -Scope <keyvault resource id> -RoleDefinitionId <role id>  -ObjectId <user/app id>

New-AzRoleAssignment -ObjectId (Get-AzADServicePrincipal -DisplayName func-hermes-proj).Id -RoleDefinitionName 'Key Vault Secrets Officer' -Scope (Get-AzResource -ResourceType "Microsoft.KeyVault/vaults" -ResourceName "kv-hermes-proj").ResourceId
```
