const axios = require("axios");

const { CLIENT_ERRORS } = require("../../httpResponseTemplates/errorTemplates");

const AUTH_SERVICE_BASE_URL =
    process.env.AUTH_SERVICE_BASE_URL || "http://127.0.0.1:8000";

const postAuthCredentials = async (req, res, endpoint) => {
    const { email, password } = req.body ?? {};

    if (!email || !password) {
        res.status(400).json({
            error: CLIENT_ERRORS.INVALID_EMAIL_OR_PW,
        });
        return null;
    }

    const payload = {
        email,
        password,
    };

    return axios.post(
        `${AUTH_SERVICE_BASE_URL}/${endpoint}`,
        payload,
        { timeout: 300000 }
    );
};

module.exports = { postAuthCredentials };
