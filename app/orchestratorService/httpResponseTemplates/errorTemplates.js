const CLIENT_ERRORS = {
    INVALID_EMAIL_OR_PW: 'invalid email or password',
    EMAIL_ALREADY_REGISTERED: "Email is already registered"
}

const SERVER_ERRORS = {
    AUTH_SERVICE_ERROR: 'Failed to reach auth service'
}

module.exports = {CLIENT_ERRORS, SERVER_ERRORS}
