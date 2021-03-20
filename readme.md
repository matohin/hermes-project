# Notes

Hermes project first prototype

## Give pipeline premissions to deploy role assignment

This project uses RBAC permissions model and creates role assignment to give function app managed identity acces to azure deviops. Azure DevOps service connection identity should be given a pemission to crete role assignment in the group, if pipeline is used to create a role assignment. Alternatives are: create role assignment manually on the portal and take it out of the template or use KeyVault access policy and disble RBAC permissions on KeyVault.

Find Azure DevOps service principle:

``` Powershell
Get-AzADServicePrincipal -DisplayName <azure DevOps organization name>*
```

Assign a role:

``` Powershell
New-AzRoleAssignment -ObjectId (Get-AzADServicePrincipal -DisplayName <Azure DevOps service connection principle name>).Id -RoleDefinitionId (Get-AzRoleDefinition -Name "User Access Administrator").Id -Scope (Get-AzResourceGroup -Name <resource group name>).ResourceId
```

## Adding secrets to the KeyVault

``` Powershell
$vaultName = 'kv-hermes-proj'
Set-AzKeyVaultSecret -VaultName $vaultName -SecretName "secretName" -SecretValue (ConvertTo-SecureString -String 'secretValuexxxyyyzzz' -AsPlainText -Force)
```

## Just useful Commands

pipenv lock -r > .\requirements.txt

gc .\.gitignore > .\.funcignore

``` Powershell

Get-AzSubscription
Get-AzResourceGroup
Get-AzRoleDefinition | Where-Object{$_.name -like "*search_for_roles*"}

New-AzRoleAssignment -Scope /subscriptions/<subscription/rg/resource id> -RoleDefinitionId <role id>  -ObjectId <user/app id>
```
