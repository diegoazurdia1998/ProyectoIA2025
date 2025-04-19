<?php
date_default_timezone_set('America/Guatemala');
function guardarHistorial($noticia, $categoria) {
    $fecha = date("Y-m-d H:i:s");
    $noticiaCorta = substr(preg_replace("/\s+/", " ", $noticia), 0, 80);

    $linea = [$fecha, $noticiaCorta, $categoria];
    $rutaCSV = '../historial.csv';

    $archivoExiste = file_exists($rutaCSV);
    $f = fopen($rutaCSV, 'a');

    if (!$archivoExiste) {
        fputcsv($f, ['Fecha y hora', 'Noticia', 'Categoría predicha'], ',', '"', '\\');
    }

    fputcsv($f, $linea, ',', '"', '\\');
    fclose($f);
}


function mostrarResultado($noticia, $categoria) {
    echo '
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Resultado del Análisis</title>
        <style>
            body {
                background-color: #f0f2f5;
                font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
                padding: 40px;
            }
            .card {
                background: white;
                max-width: 800px;
                margin: auto;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            }
            h2 {
                color: #333;
                margin-top: 0;
            }
            .noticia, .categoria {
                margin-bottom: 30px;
            }
            .categoria strong {
                font-size: 20px;
                color: #0066cc;
            }
            button {
                padding: 10px 20px;
                background-color: #0066cc;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;
                transition: background-color 0.3s;
            }
            button:hover {
                background-color: #004a99;
            }
            .volver {
                display: flex;
                justify-content: center;
                gap: 20px;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <div class="noticia">
                <h2>📰 Noticia:</h2>
                <p>' . nl2br(htmlspecialchars($noticia)) . '</p>
            </div>
            <div class="categoria">
                <h2>🔍 Categoría predicha:</h2>
                <strong>' . htmlspecialchars($categoria) . '</strong>
            </div>
            <div class="volver">
                <a href="index.html" style="text-decoration: none;">
                    <button>📤 Subir otra noticia</button>
                </a>
                <a href="historial.php" style="text-decoration: none;">
                    <button style="background-color: #888;">📜 Ver historial</button>
                </a>
            </div>
        </div>
    </body>
    </html>';
}


if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    if (isset($_FILES['archivo']) && $_FILES['archivo']['error'] == 0) {
        $nombreArchivo = $_FILES['archivo']['name'];
        $extension = pathinfo($nombreArchivo, PATHINFO_EXTENSION);

        if ($extension != 'txt') {
            die("Solo se permiten archivos .txt");
        }

        $rutaDestino = 'uploads/' . basename($nombreArchivo);
        if (!file_exists('uploads')) {
            mkdir('uploads', 0777, true);
        }

        if (move_uploaded_file($_FILES['archivo']['tmp_name'], $rutaDestino)) {
            $contenido = file_get_contents($rutaDestino);
            $contenidoEscapado = escapeshellarg($contenido);
            $rutaPython = '../NaiveBayes.py';
            $categoria = trim(shell_exec("python $rutaPython $contenidoEscapado"));
            guardarHistorial($contenido, $categoria);
            mostrarResultado($contenido, $categoria);
        } else {
            echo "Error al subir el archivo.";
        }
    } else {
        echo "No se seleccionó ningún archivo o hubo un error.";
    }
}
?>
