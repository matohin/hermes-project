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

    Write-Debug -Message "KeyVaultName: $KeyVaultName"
    Write-Debug -Message "MandatorySecretsList: $MandatorySecretsList"

    $KeyVaultObject = Get-AzResource -ResourceType Microsoft.KeyVault/vaults -Name $KeyVaultName
    if (!$KeyVaultObject) { Throw "KeyVault $KeyVaultName is not deployed, it should exist prior to main pipeline deployment" }

    foreach ($SecrenName in $MandatorySecretsList)
    {
        $CurrentSecret = Get-AzKeyVaultSecret -VaultName $KeyVaultName -Name $SecrenName
        if (!$CurrentSecret) { Throw "Secret $SecrenName is not created in $KeyVaultName. Please consult readme and fill KeyVault with mandatory secrets before running main pipeline." }
    }
}
