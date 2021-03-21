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

    $TelegramApiUrl = "https://api.telegram.org/$TelegramBotToken/setWebhook"

    $WebhookUrl = "https://$FunctionAppName.azurewebsites.net/api/input_trunk_telegram?code=$FunctionKey"
    $RequestBody = (@{url = $WebhookUrl } | ConvertTo-Json)

    Invoke-WebRequest -Uri $TelegramApiURL -Method Post -ContentType "application/json" -Body $RequestBody
}
