<?php
date_default_timezone_set('America/Guatemala');
$rutaCSV = '../historial.csv';
$datos = [];

// Evita errores "Deprecated" usando los 5 parámetros de fgetcsv
if (file_exists($rutaCSV) && filesize($rutaCSV) > 0) {
    $f = fopen($rutaCSV, 'r');
    while (($fila = fgetcsv($f, 1000, ",", '"', "\\")) !== false) {
        $datos[] = $fila;
        // Separar encabezado y datos, luego invertir solo los datos
        $encabezado = $datos[0];
        $filas = array_slice($datos, 1);
        $filas = array_reverse($filas);
        $datos = array_merge([$encabezado], $filas);

    }
    fclose($f);
}
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Historial de Noticias Clasificadas</title>
    <style>
        body {
            background-color: #f0f2f5;
            font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
            padding: 40px;
        }
        .container {
            max-width: 900px;
            margin: auto;
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }
        h1 {
            text-align: center;
            color: #333;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 30px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        th {
            background-color: #0066cc;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        .volver {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 30px;
        }
        .volver a button {
            text-decoration: none;
            background-color: #0066cc;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .volver a button:hover {
            background-color: #004a99;
        }
        .volver a:nth-child(2) button {
            background-color: #28a745;
        }
        .volver a:nth-child(2) button:hover {
            background-color: #1e7e34;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📜 Historial de Noticias Clasificadas</h1>

        <?php if (count($datos) > 1): ?>
            <table>
                <tr>
                    <?php foreach ($datos[0] as $col): ?>
                        <th><?php echo htmlspecialchars($col); ?></th>
                    <?php endforeach; ?>
                </tr>
                <?php for ($i = 1; $i < count($datos); $i++): ?>
                    <tr>
                        <?php foreach ($datos[$i] as $valor): ?>
                            <td><?php echo htmlspecialchars($valor); ?></td>
                        <?php endforeach; ?>
                    </tr>
                <?php endfor; ?>
            </table>
        <?php else: ?>
            <p style="text-align:center; margin-top: 40px;">No hay registros aún.</p>
        <?php endif; ?>

        <div class="volver">
            <a href="index.html"><button>📤 Subir otra noticia</button></a>
            <a href="../historial.csv" download><button>⬇️ Descargar CSV</button></a>
        </div>
    </div>
</body>
</html>
