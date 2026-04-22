const express = require('express');
const axios = require("axios");
const path = require("path");
require("dotenv").config({ path: path.join(__dirname, ".env") });

const { CLIENT_ERRORS, SERVER_ERRORS } = require('./httpResponseTemplates/errorTemplates');
const verifyAccessToken = require("./utils/authService/verifyAccessToken");

const app = express();
const port = process.env.PORT || 5000;
const AUTH_SERVICE_BASE_URL =
    process.env.AUTH_SERVICE_BASE_URL || "http://127.0.0.1:8000";

app.use(express.json({ limit: "1mb" }));

app.get('/', (req, res) => {
    // res.send({res:'scuccess'});
    res.status(200).json({
        res: 'sucess'
    });
});

app.post('/auth/login', async (req, res) => {
    try {
        console.log(req.body);
        const { email, password } = req.body ?? {};

        if (!email || !password) {
            return res.status(400).json({
                error: CLIENT_ERRORS.INVALID_LOGIN
            })
        }
        const payload = {
            email,
            password
        }
        const response = await axios.post(
            `${AUTH_SERVICE_BASE_URL}/login`,
            payload,
            { timeout: 300000 } // 5 min
        )
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
                error: CLIENT_ERRORS.INVALID_LOGIN,
            });
        }
        console.error("Login proxy failed:", error);
        return res.status(502).json({
            error: SERVER_ERRORS.AUTH_SERVICE_ERROR,
        });
    }
});

app.post('/auth/refresh', async (req, res) => {
    try {
        const response = await axios.post(
            `${AUTH_SERVICE_BASE_URL}/refresh`,
            req.body,
            { timeout: 300000 }
        );

        return res.status(200).json({
            source: "orchestrator",
            data: response.data ?? null,
        });
    } catch (error) {
        return res.status(error.response?.status || 502).json({
            error: error.response?.data?.detail || "Failed to refresh token",
        });
    }
});

app.post('/user/ingest', verifyAccessToken, async (req, res) => {
    return res.status(200).json({
        message: "Token verified. User ingest can continue.",
        user: req.user,
        payload: req.body ?? null,
    });
});

app.listen(port, () => {
    console.log(`Orchestrator service running on port ${port}`);
});
