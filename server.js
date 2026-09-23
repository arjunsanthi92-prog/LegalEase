const express = require("express");
const OpenAI = require("openai");
require("dotenv").config();

const app = express();
const port = 3000;

const client = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY
});

app.use(express.json());
app.use(express.static(__dirname));

app.post("/api/ask", async (req, res) => {
    try {
        const question = req.body.question;

        if (!question || !question.trim()) {
            return res.status(400).json({
                error: "Please enter a legal question."
            });
        }

        const response = await client.responses.create({
            model: "gpt-5.6-luna",
            instructions:
                "You are LegalEase AI, a legal information assistant. " +
                "Give clear and simple general legal information. " +
                "Do not pretend to be a lawyer. " +
                "Mention that laws vary by country or jurisdiction when relevant. " +
                "Do not provide definitive personalized legal advice.",
            input: question
        });

        res.json({
            answer: response.output_text
        });

    } catch (error) {
        console.error("OpenAI Error:", error);

        res.status(500).json({
            error: "Unable to get an AI response."
        });
    }
});

app.listen(port, () => {
    console.log(`LegalEase running at http://localhost:${port}`);
});