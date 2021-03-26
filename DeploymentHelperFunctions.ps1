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

function Test-KeyVaultReadines
{
    param (
        [Parameter(Mandatory = $true)]
        [string]
        $KeyVaultName,
        [Parameter(Mandatory = $true)]
        [string[]]
        $MandatorySecretsList
    )

    try
    {

    }
    catch
    {

    }
    finally
    {

    }
}