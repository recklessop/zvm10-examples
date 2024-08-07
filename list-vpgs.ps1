
# Configuration variables
$ZVM_ADDRESS = $env:ZVM_ADDRESS
if (-not $ZVM_ADDRESS) {
    $ZVM_ADDRESS = "172.16.50.100"
}
$ZVM_USERNAME = $env:ZVM_USERNAME
if (-not $ZVM_USERNAME) {
    $ZVM_USERNAME = "admin"
}
$ZVM_PASSWORD = $env:ZVM_PASSWORD
if (-not $ZVM_PASSWORD) {
    $ZVM_PASSWORD = "Zertodata987!"
}
$VERIFY_CERTIFICATE = false

# Nothing below should need modified for the example to run and list VPGs

$KEYCLOAK_API_BASE = "https://$ZVM_ADDRESS/auth/realms/zerto/protocol/openid-connect/token"
$ZVM_API_BASE = "https://$ZVM_ADDRESS/v1/"

# Configure logging
function Write-Log {
    param (
        [string]$message,
        [string]$level = "INFO"
    )
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Output "$timestamp - $level - $message"
}

# Function to get a token from Keycloak
function Get-Token {
    $uri = $KEYCLOAK_API_BASE
    $headers = @{
        'Content-Type' = 'application/x-www-form-urlencoded'
    }
    $body = @{
        'username'  = $ZVM_USERNAME
        'password'  = $ZVM_PASSWORD
        'grant_type' = 'password'
        'client_id' = 'zerto-client'
    }

    try {
        $response = Invoke-RestMethod -Uri $uri -Headers $headers -Method Post -Body $body -SkipCertificateCheck:$VERIFY_CERTIFICATE
        return $response.access_token
    }
    catch {
        Write-Log "Error obtaining token: $_" "ERROR"
        return $null
    }
}

# Main function which executes when the program is run
function Run {
    # Authenticate to the ZVM
    $token = Get-Token
    if (-not $token) {
        Write-Log "Failed to get token." "ERROR"
        return
    }

    # This line can be adjusted to any API URL in ZVM
    $uri = $ZVM_API_BASE + "vpgs"
    $headers = @{
        'Content-Type' = 'application/json'
        'Authorization' = "Bearer $token"
    }

    try {
        # This line will need to be modified depending on if the API you want is a GET, POST, PUT, DELETE, etc.
        $response = Invoke-RestMethod -Uri $uri -Headers $headers -Method Get -SkipCertificateCheck:$VERIFY_CERTIFICATE
        Write-Log "Request successful.`n$($response | ConvertTo-Json)"
    }
    catch {
        Write-Log "Request to Zerto API failed: $_" "ERROR"
    }
}

# Execute the main function
Run
