const { CLIENT_ERRORS, SERVER_ERRORS } = require("../../httpResponseTemplates/errorTemplates");
const { postAuthCredentials } = require("../utils/authCredentialProxy");

const login = (async (req, res) => {
    try {
        const response = await postAuthCredentials(req, res, "login");
        if (response === null) return;

        console.log(response.data);
        return res.status(200).json({
            source: "orchestrator",
            data: response.data ?? null,
        });
    } catch (error) {
        const statusCode = error.response?.status;
        const errorDetail = error.response?.data?.detail;

        if (statusCode === 403) {
            return res.status(403).json({
                error: errorDetail ?? "User account is not active",
            });
        }

        if (statusCode === 422 || statusCode === 401) {
            return res.status(400).json({
                error: CLIENT_ERRORS.INVALID_EMAIL_OR_PW,
            });
        }

        console.error("Login proxy failed:", error);
        return res.status(502).json({
            error: SERVER_ERRORS.AUTH_SERVICE_ERROR,
        });
    }
});

module.exports = { login };
