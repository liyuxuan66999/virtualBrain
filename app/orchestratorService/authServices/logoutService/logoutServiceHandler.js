const axios = require("axios");

const AUTH_SERVICE_BASE_URL =
    process.env.AUTH_SERVICE_BASE_URL || "http://127.0.0.1:8000";

const logout = (async (req, res) => {
    try {
        const response = await axios.post(
            `${AUTH_SERVICE_BASE_URL}/logout`,
            req.body,
            { timeout: 300000 }
        );

        return res.status(200).json({
            source: "orchestrator",
            data: response.data ?? null,
        });
    } catch (error) {
        return res.status(error.response?.status || 502).json({
            error: error.response?.data?.detail || "Failed to logout",
        });
    }
});

module.exports = { logout };
