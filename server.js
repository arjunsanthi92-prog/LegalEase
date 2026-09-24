const express = require("express");
const { GoogleGenAI } = require("@google/genai");
require("dotenv").config();

const app = express();
const port = 3000;

const client = new GoogleGenAI({
    apiKey: process.env.GEMINI_API_KEY
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

        const response = await client.models.generateContent({
            model: "gemini-3.5-flash-lite",
            contents: question,
            config: {
                systemInstruction:
                    "You are LegalEase AI, a legal information assistant. " +
                    "Give clear and simple general legal information. " +
                    "Do not pretend to be a lawyer. " +
                    "Mention that laws vary by country or jurisdiction when relevant. " +
                    "Do not provide definitive personalized legal advice."
            }
        });

        res.json({
            answer: response.text
        });

    } catch (error) {
        console.error("Gemini Error:", error);

        res.status(500).json({
            error: "Unable to get an AI response."
        });
    }
});

const server = app.listen(port, () => {
    console.log(`LegalEase running at http://localhost:${port}`);
});

server.on("error", (error) => {
    console.error("Server Error:", error);
});