const jwt = require("jsonwebtoken");

const JWT_SECRET = process.env.JWT_SECRET || "dev-secret-only";
const JWT_ALGORITHM = process.env.JWT_ALGORITHM || "HS256";

const verifyAccessToken = (req, res, next) => {
    const authHeader = req.headers.authorization;
    console.log("JWT_SECRET:", JWT_SECRET);
    console.log("JWT_ALGORITHM:", JWT_ALGORITHM);
    if (!authHeader || !authHeader.startsWith("Bearer ")) {
        return res.status(401).json({
            error: "Missing or invalid Authorization header",
        });
    }

    const token = authHeader.split(" ")[1];

    try {
        const decoded = jwt.verify(token, JWT_SECRET, {
            algorithms: [JWT_ALGORITHM],
        });

        if (decoded.type !== "access") {
            return res.status(401).json({
                error: "Invalid token type",
            });
        }
        console.log(`decoded JWT: user:${decoded.sub}, email:${decoded.email} `)
        req.user = {
            userId: decoded.sub,
            email: decoded.email,
            tokenType: decoded.type,
        };

        return next();
    } catch (error) {
        console.log("JWT verify error:", error.message);
        return res.status(401).json({
            error: error.name === "TokenExpiredError"
                ? "Token expired"
                : "Invalid token",
        });
    }
};

module.exports = verifyAccessToken;
