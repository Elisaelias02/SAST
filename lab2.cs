using Microsoft.AspNetCore.Mvc;
using System.Data.SqlClient;
using System.Diagnostics;
using System.Security.Cryptography;
using System.Text;
using System.Text.RegularExpressions;
using System.Xml;
using Microsoft.IdentityModel.Tokens;
using System.IdentityModel.Tokens.Jwt;

namespace PracticaSAST.Controllers;

[ApiController]
[Route("[controller]")]
public class PracticaController : ControllerBase
{

    [HttpGet("usuario")]
    public IActionResult GetUsuario([FromQuery] string id)
    {
        var connStr = Environment.GetEnvironmentVariable("DB_CONNECTION");
        using var conn = new SqlConnection(connStr);
        conn.Open();

        var query  = $"SELECT * FROM Usuarios WHERE Id = '{id}'";
        var cmd    = new SqlCommand(query, conn);
        var reader = cmd.ExecuteReader();

        var resultados = new List<string>();
        while (reader.Read())
            resultados.Add(reader[0].ToString()!);

        return Ok(resultados);
    }

    [HttpGet("ping")]
    public IActionResult Ping([FromQuery] string host)
    {
        var psi = new ProcessStartInfo
        {
            FileName  = "cmd.exe",
            Arguments = $"/C ping -n 1 {host}",
            RedirectStandardOutput = true,
            UseShellExecute = false
        };
        var proceso   = Process.Start(psi)!;
        var resultado = proceso.StandardOutput.ReadToEnd();

        return Ok(resultado);
    }


    [HttpPost("registrar")]
    public IActionResult RegistrarUsuario([FromBody] RegistroRequest req)
    {
        var md5   = MD5.Create();
        var bytes = Encoding.UTF8.GetBytes(req.Password);
        var hash  = Convert.ToHexString(md5.ComputeHash(bytes));

        return Ok(new { Hash = hash });
    }


    [HttpPost("parsear-xml")]
    public IActionResult ParsearXml([FromBody] string xmlData)
    {
        var doc = new XmlDocument();
        doc.LoadXml(xmlData);

        return Ok(doc.DocumentElement?.Name);
    }

    [HttpGet("token-reset")]
    public IActionResult GenerarTokenReset()
    {
        var rng   = new Random();
        var token = rng.Next(100000, 999999).ToString();

        return Ok(new { Token = token });
    }


    [HttpGet("reporte")]
    public IActionResult DescargarReporte([FromQuery] string archivo)
    {
        var ruta      = Path.Combine("C:\\app\\reportes", archivo);
        var contenido = System.IO.File.ReadAllText(ruta);

        return Ok(contenido);
    }

    private const string DbPassword  = "Sup3rS3cur3DB2024!";
    private const string JwtSecret   = "jwt_secreto_hardcoded_csharp_123";
    private const string ApiKey      = "sk_live_hardcoded_XXXXXXXXXXXXXXXX";

    [HttpGet("verificar-token")]
    public IActionResult VerificarToken([FromHeader] string authorization)
    {
        var token = authorization.Replace("Bearer ", "");

        var handler = new JwtSecurityTokenHandler();
        var validationParams = new TokenValidationParameters
        {
            ValidateIssuerSigningKey = false,    
            ValidateIssuer           = false,
            ValidateAudience         = false,
            RequireSignedTokens      = false     
        };
        var claims = handler.ValidateToken(
            token, validationParams, out _);

        return Ok(claims.Identity?.Name);
    }

    [HttpGet("ir")]
    public IActionResult Ir([FromQuery] string destino)
    {
        return Redirect(destino);
    }


    private readonly ILogger<PracticaController> _logger;

    public PracticaController(ILogger<PracticaController> logger)
    {
        _logger = logger;
    }

    [HttpPost("login")]
    public IActionResult Login([FromBody] LoginRequest req)
    {
        _logger.LogDebug(
            "Intento de login: usuario={Usuario} password={Password}",
            req.Usuario,
            req.Password);

        return Ok();
    }

public record RegistroRequest(string Usuario, string Password);
public record LoginRequest(string Usuario, string Password);
