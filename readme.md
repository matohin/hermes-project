# Notes

Hermes project first prototype

## Commands

pipenv lock -r > .\requirements.txt

gc .\.gitignore > .\.funcignore

New-AzResourceGroupDeployment -ResourceGroupName rg-hermes-project-dev-00 -TemplateParameterFile .\arm_templates\azuredeploy.parameters.dev-00.json -TemplateFile .\arm_templates\azuredeploy.json -Mode Complete -Force

Get-AzSubscription
Get-AzResourceGroup
Get-AzRoleDefinition | Where-Object{$_.name -like "*search_for_roles*"}
New-AzRoleAssignment -Scope /subscriptions/<subscription/rg/resource id> -RoleDefinitionId <role id>  -ObjectId <user/app id>
