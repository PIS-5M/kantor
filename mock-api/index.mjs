import express from "express";
import cors from "cors";

const app = express();
app.use(cors());
app.use(express.json());
const PORT = process.env.PORT || 8000;
app.get("/", (req, res) => res.json({ message: "Guten morgen" }));

app.post("/login", (req, res) => {
  return res.json({ id: 1 });
});

app.listen(PORT, () => {
  console.log(`mock server listening at 0.0.0.0:${PORT}`);
});
