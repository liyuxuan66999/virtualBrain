const express = require('express');
const path = require("path");
require("dotenv").config({ path: path.join(__dirname, ".env") });

const verifyAccessToken = require("./utils/authService/verifyAccessToken");
const { register: handleRegister } = require("./authServices/registerService/registerServiceHandler");
const { login: handleLogin } = require("./authServices/loginService/loginServiceHandler");
const { refresh: handleRefresh } = require("./authServices/refreshService/refreshServiceHandler");
const { logout: handleLogout } = require("./authServices/logoutService/logoutServiceHandler");
const { ingest: handleIngest } = require("./userServices/ingestService/ingestServiceHandler");

const app = express();
const port = process.env.PORT || 5000;

app.use(express.json({ limit: "1mb" }));

app.get('/', (req, res) => {
    // res.send({res:'scuccess'});
    res.status(200).json({
        res: 'sucess'
    });
});

app.post('/auth/register', handleRegister);

app.post('/auth/login', handleLogin);

app.post('/auth/refresh', handleRefresh);

app.post('/auth/logout', handleLogout);

app.post('/user/ingest', verifyAccessToken, handleIngest);

app.listen(port, () => {
    console.log(`Orchestrator service running on port ${port}`);
});
