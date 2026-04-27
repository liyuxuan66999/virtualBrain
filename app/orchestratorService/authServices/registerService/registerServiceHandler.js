const { CLIENT_ERRORS, SERVER_ERRORS } = require("../../httpResponseTemplates/errorTemplates");
const { postAuthCredentials } = require("../utils/authCredentialProxy");

const register = (async (req, res) => {
    try {
        const response = await postAuthCredentials(req, res, "register");
        if (response === null) return;

        return res.status(201).json({
            source: "orchestrator",
            data: response.data ?? null,
        });
    } catch (error) {
        const statusCode = error.response?.status;
        const errorDetail = error.response?.data?.detail;

        if (statusCode === 409) {
            return res.status(409).json({
                error: errorDetail ?? CLIENT_ERRORS.EMAIL_ALREADY_REGISTERED,
            });
        }

        if (statusCode === 422) {
            return res.status(400).json({
                error: CLIENT_ERRORS.INVALID_EMAIL_OR_PW,
            });
        }

        console.error("Register proxy failed:", error);
        return res.status(502).json({
            error: SERVER_ERRORS.AUTH_SERVICE_ERROR,
        });
    }
})

module.exports = {register};
