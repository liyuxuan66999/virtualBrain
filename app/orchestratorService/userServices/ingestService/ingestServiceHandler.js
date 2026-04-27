const ingest = (async (req, res) => {
    return res.status(200).json({
        message: "Token verified. User ingest can continue.",
        user: req.user,
        payload: req.body ?? null,
    });
});

module.exports = { ingest };
