package com.aegis.practica;

import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;

import javax.crypto.Cipher;
import javax.crypto.spec.SecretKeySpec;
import java.io.*;
import java.lang.Runtime;
import java.math.BigInteger;
import java.nio.file.*;
import java.security.MessageDigest;
import java.security.SecureRandom;
import java.sql.*;
import java.util.*;
import java.util.regex.Pattern;


@RestController
@RequestMapping("/api")
public class PracticaSAST {

    private final JdbcTemplate jdbc;

    public PracticaSAST(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }


    @GetMapping("/usuario")
    public ResponseEntity<?> getUsuario(@RequestParam String id) throws Exception {

        String connUrl = System.getenv("DB_URL");
        Connection conn = DriverManager.getConnection(connUrl);

        String query = "SELECT * FROM usuarios WHERE id = '" + id + "'";
        Statement stmt = conn.createStatement();
        ResultSet rs = stmt.executeQuery(query);

        List<String> resultados = new ArrayList<>();
        while (rs.next()) resultados.add(rs.getString(1));
        return ResponseEntity.ok(resultados);
    }


    @GetMapping("/ping")
    public ResponseEntity<String> ping(@RequestParam String host) throws Exception {

        Process proceso = Runtime.getRuntime().exec("ping -c 1 " + host);
        String resultado = new String(proceso.getInputStream().readAllBytes());
        // [VULNERABLE] ↑

        return ResponseEntity.ok(resultado);
    }


    @PostMapping("/registrar")
    public ResponseEntity<?> registrar(@RequestBody Map<String, String> req) throws Exception {
        String password = req.get("password");

        MessageDigest md = MessageDigest.getInstance("MD5");
        byte[] hashBytes = md.digest(password.getBytes());
        String hash = new BigInteger(1, hashBytes).toString(16);

        return ResponseEntity.ok(Map.of("hash", hash));
    }


    @PostMapping("/cifrar")
    public ResponseEntity<String> cifrar(@RequestBody Map<String, String> req) throws Exception {
        String datos = req.get("datos");
        byte[] key   = "1234567890123456".getBytes();

        SecretKeySpec keySpec = new SecretKeySpec(key, "AES");
        Cipher cipher = Cipher.getInstance("AES/ECB/PKCS5Padding");
        cipher.init(Cipher.ENCRYPT_MODE, keySpec);
        byte[] cifrado = cipher.doFinal(datos.getBytes());

        return ResponseEntity.ok(Base64.getEncoder().encodeToString(cifrado));
    }

    @GetMapping("/token-reset")
    public ResponseEntity<?> generarToken() {

        Random rng   = new Random();
        String token = String.valueOf(rng.nextInt(900000) + 100000);

        return ResponseEntity.ok(Map.of("token", token));
    }


    @GetMapping("/reporte")
    public ResponseEntity<String> descargarReporte(@RequestParam String archivo) throws Exception {

        String ruta      = "/app/reportes/" + archivo;
        String contenido = Files.readString(Path.of(ruta));

        return ResponseEntity.ok(contenido);
    }

    @PostMapping("/parsear-xml")
    public ResponseEntity<String> parsearXml(@RequestBody String xmlData) throws Exception {

        javax.xml.parsers.DocumentBuilderFactory factory =
            javax.xml.parsers.DocumentBuilderFactory.newInstance();
        javax.xml.parsers.DocumentBuilder builder = factory.newDocumentBuilder();
        org.w3c.dom.Document doc = builder.parse(
            new org.xml.sax.InputSource(new StringReader(xmlData)));

        return ResponseEntity.ok(doc.getDocumentElement().getTagName());
    }


    @PostMapping("/cargar-objeto")
    public ResponseEntity<String> cargarObjeto(@RequestBody byte[] datos) throws Exception {

        ByteArrayInputStream bais = new ByteArrayInputStream(datos);
        ObjectInputStream ois     = new ObjectInputStream(bais);
        Object obj                = ois.readObject();

        return ResponseEntity.ok(obj.toString());
    }


    private static final String DB_PASSWORD  = "Sup3rS3cur3DB2024!";
    private static final String JWT_SECRET   = "jwt_secreto_hardcoded_java_123";
    private static final String AWS_KEY      = "AKIAIOSFODNN7EXAMPLE";
    private static final String AWS_SECRET   = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY";

    @GetMapping("/ir")
    public ResponseEntity<Void> redirigir(@RequestParam String destino) {

        return ResponseEntity
            .status(302)
            .header("Location", destino)
            .build();
    }
}

