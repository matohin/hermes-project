# Notes

Hermes project first prototype

## Give pipeline premissions to deploy role assignment

This project uses RBAC permissions model and creates role assignment to give function app managed identity acces to azure deviops. Azure DevOps service connection identity should be given a pemission to crete role assignment in the group, if pipeline is used to create a role assignment. Alternatives are: create role assignment manually on the portal and take it out of the template or use KeyVault access policy and disble RBAC permissions on KeyVault.

Find Azure DevOps service principle:
`Get-AzADServicePrincipal -DisplayName <azure DevOps organization namr>*`

Assign a role:
`New-AzRoleAssignment -ObjectId (Get-AzADServicePrincipal -DisplayName <Azure DevOps service connection principle name>).Id -RoleDefinitionId (Get-AzRoleDefinition -Name "User Access Administrator").Id -Scope (Get-AzResourceGroup -Name <resource group name>).ResourceId`

## Useful Commands

pipenv lock -r > .\requirements.txt

gc .\.gitignore > .\.funcignore


``` Powershell
New-AzResourceGroupDeployment -ResourceGroupName rg-hermes-project-dev-00 -TemplateParameterFile .\arm_templates\azuredeploy.parameters.dev-00.json -TemplateFile .\arm_templates\azuredeploy.json -Mode Complete -Force

Get-AzSubscription
Get-AzResourceGroup
Get-AzRoleDefinition | Where-Object{$_.name -like "*search_for_roles*"}

New-AzRoleAssignment -Scope /subscriptions/<subscription/rg/resource id> -RoleDefinitionId <role id>  -ObjectId <user/app id>
```
