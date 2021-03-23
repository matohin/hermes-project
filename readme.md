# Notes

Hermes project first prototype

## Give pipeline premissions to deploy role assignment

This project uses RBAC permissions model and creates role assignment to give function app managed identity acces to azure deviops. Azure DevOps service connection identity should be given a pemission to create role assignment in the group, if pipeline is used to create a role assignment. Alternatives are: create role assignment manually on the portal and take it out of the template or use KeyVault access policy and disable RBAC permissions on KeyVault.

Find Azure DevOps service principle:

``` Powershell
$PiplineServicePrincipal = Get-AzADServicePrincipal -ApplicationId <application ID of connection SP> # Id can be looked up at connection settings
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

## Just useful Commands

pipenv lock -r > .\requirements.txt

``` Powershell
gc .\.gitignore > .\.funcignore

Get-AzSubscription
Get-AzResourceGroup
Get-AzRoleDefinition | Where-Object{$_.name -like "*search_for_roles*"}

New-AzRoleAssignment -Scope <keyvault resource id> -RoleDefinitionId <role id>  -ObjectId <user/app id>

New-AzRoleAssignment -ObjectId (Get-AzADServicePrincipal -DisplayName func-hermes-proj).Id -RoleDefinitionName 'Key Vault Secrets Officer' -Scope (Get-AzResource -ResourceType "Microsoft.KeyVault/vaults" -ResourceName "kv-hermes-proj").ResourceId
```
