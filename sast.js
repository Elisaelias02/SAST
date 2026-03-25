const express = require("express");
const { execSync, exec } = require("child_process");
const crypto  = require("crypto");
const fs      = require("fs");
const path    = require("path");
const http    = require("http");
const https   = require("https");

const app = express();
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

const sqlite3 = require("sqlite3").verbose();
const db = new sqlite3.Database(":memory:");

app.get("/usuario", (req, res) => {
  const userId = req.query.id;

  const query = `SELECT * FROM usuarios WHERE id = '${userId}'`;
  db.all(query, (err, rows) => {
    res.json(rows);
  });
});


app.get("/ping", (req, res) => {
  const host = req.query.host;

  const resultado = execSync(`ping -c 1 ${host}`).toString();

  res.send(resultado);
});


app.get("/saludo", (req, res) => {
  const nombre = req.query.nombre;

  res.send(`<h1>Hola, ${nombre}</h1>`);
});

app.get("/reporte", (req, res) => {
  const archivo = req.query.archivo;

  const ruta = path.join("/app/reportes", archivo);
  const contenido = fs.readFileSync(ruta, "utf8");
  res.send(contenido);
});


app.post("/validar-email", (req, res) => {
  const email = req.body.email;

  const regex = /^([a-zA-Z0-9])+([a-zA-Z0-9._-])*@([a-zA-Z0-9_-])+([a-zA-Z0-9._-]+)+$/;
  const valido = regex.test(email);
  res.json({ valido });
});


app.post("/calcular", (req, res) => {
  const expresion = req.body.expresion;

  // [VULNERABLE] ↓
  const resultado = eval(expresion);
  // [VULNERABLE] ↑

  res.json({ resultado });
});


app.get("/ir", (req, res) => {
  const destino = req.query.destino;

  res.redirect(destino);
});

const DB_PASSWORD     = "Sup3rS3cur3DB2024!";
const JWT_SECRET      = "jwt_secreto_hardcoded_123";
const AWS_ACCESS_KEY  = "AKIAIOSFODNN7EXAMPLE";
const AWS_SECRET_KEY  = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY";

const jwt = require("jsonwebtoken");

app.get("/verificar-token", (req, res) => {
  const token = req.headers.authorization?.replace("Bearer ", "");

  const decoded = jwt.verify(token, JWT_SECRET, { algorithms: ["HS256", "none"] });

  res.json(decoded);
});


app.get("/set-sesion", (req, res) => {
  const userId = req.query.id;

  res.cookie("session_id", userId);

  res.json({ status: "ok" });
});


app.listen(3000, () => console.log("Servidor en http://localhost:3000"));
