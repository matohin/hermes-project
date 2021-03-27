function Register-TelegramWebhookUrl
{
    param (
        [Parameter(Mandatory = $true)]
        [string]$TelegramBotToken,
        [Parameter(Mandatory = $true)]
        [string]$FunctionAppName,
        [Parameter(Mandatory = $true)]
        [string]$FunctionKey
    )

    $TelegramApiUrl = "https://api.telegram.org/bot$TelegramBotToken/setWebhook"
    Write-Debug -Message "API url: $TelegramApiUrl"


    $WebhookUrl = "https://$FunctionAppName.azurewebsites.net/api/input_trunk_telegram?code=$FunctionKey"
    $RequestBody = (@{url = $WebhookUrl } | ConvertTo-Json)
    Write-Debug -Message "Request body: $RequestBody"

    $Response = Invoke-RestMethod -Uri $TelegramApiURL -Method Post -ContentType "application/json" -Body $RequestBody
    Write-Debug -Message "API response: $Response"
}

function Test-KeyVaultReadiness
{
    param (
        [Parameter(Mandatory = $true)]
        [string]$KeyVaultName,
        [Parameter(Mandatory = $true)]
        [string[]]$MandatorySecretsList
    )

    $KeyVaultObject = Get-AzResource -ResourceType Microsoft.KeyVault/vaults -Name hermes-proj-keyvault
    if (!$KeyVaultObject) { Throw "KeyVault is not deployed, it should exist prior to main pipeline deployment" }

    foreach ($SecrenName in $MandatorySecretsList)
    {
        $CurrentSecret = Get-AzKeyVaultSecret -VaultName $KeyVaultName -Name $SecrenName
        if (!$CurrentSecret) { Throw "Secret $CurrentSecret is not created in. Please consult readme and fill KeyVault with mandatory secrets before running main pipeline." }
    }
}

function Clear-ManagedIdentityRoleAssignment
{
    param (
        [Parameter(Mandatory = $true)]
        [string]$FunctionAppName,
        [Parameter(Mandatory = $true)]
        [string]$ResourceGroupName,
        [Parameter(Mandatory = $true)]
        [string]$AssignmentDefinitionMarker
    )

    $FunctionApp = Get-AzFunctionApp -Name $FunctionAppName -ResourceGroupName $ResourceGroupName
    Write-Debug -Message "Function App object $FunctionApp"
    $ManagedIdentityRoleAssignment = Get-AzRoleAssignment -ResourceGroupName $ResourceGroupName | Where-Object { $_.Description -eq $AssignmentDefinitionMarker }
    Write-Debug -Message "Role Assignment object $ManagedIdentityRoleAssignment"

    if (!$FunctionApp -and $ManagedIdentityRoleAssignment)
    {
        $ManagedIdentityRoleAssignment | Remove-AzRoleAssignment
        Write-Debug -Message "Function App not found, removing $ManagedIdentityRoleAssignment"
    }

    elseif ($ManagedIdentityRoleAssignment -and ($FunctionApp.IdentityPrincipalId -ne $ManagedIdentityRoleAssignment.ObjectId))
    {
        $ManagedIdentityRoleAssignment | Remove-AzRoleAssignment
        Write-Debug -Message "Principal mismatch found in assignment with a known description marker, removing $ManagedIdentityRoleAssignment"
    }
}
