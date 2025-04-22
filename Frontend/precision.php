<?php
ini_set('display_errors', 1);
error_reporting(E_ALL);

$rutaPython = '../NaiveBayes.py';
$json = shell_exec("python $rutaPython 2>&1");
$data = json_decode($json, true);

// Validar la respuesta
if (!$data || !isset($data['accuracy'])) {
    die("<h2 style='color:red;'>❌ Error al obtener datos del modelo. Respuesta inválida:</h2><pre>$json</pre>");
}
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Precisión del Modelo</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {
            background-color: #f4f4f4;
            font-family: Arial, sans-serif;
            padding: 30px;
        }
        .container {
            max-width: 900px;
            margin: auto;
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            text-align: center;
        }
        canvas {
            margin-top: 30px;
        }
        .volver {
            margin-top: 40px;
        }
        .volver a {
            text-decoration: none;
            background-color: #0066cc;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
        }
        .volver a:hover {
            background-color: #004a99;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Precisión del Modelo</h1>
        <p>🔍 Precisión general: <strong><?php echo $data['accuracy'] * 100; ?>%</strong></p>
        <canvas id="chart" width="800" height="400"></canvas>

        <div class="volver">
            <a href="historial.php">🔙 Volver al historial</a>
        </div>
    </div>

    <script>
        const data = <?php echo json_encode($data['report']); ?>;
        const labels = [];
        const precision = [];
        const recall = [];
        const f1 = [];

        for (const clase in data) {
            if (['accuracy', 'macro avg', 'weighted avg'].includes(clase)) continue;
            labels.push(clase);
            precision.push(data[clase]['precision']);
            recall.push(data[clase]['recall']);
            f1.push(data[clase]['f1-score']);
        }

        const ctx = document.getElementById('chart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Precisión',
                        data: precision,
                        backgroundColor: '#007bff'
                    },
                    {
                        label: 'Recall',
                        data: recall,
                        backgroundColor: '#28a745'
                    },
                    {
                        label: 'F1-Score',
                        data: f1,
                        backgroundColor: '#ffc107'
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.dataset.label}: ${(context.parsed.y * 100).toFixed(2)}%`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        min: 0,
                        max: 1,
                        ticks: {
                            callback: val => (val * 100) + '%'
                        }
                    }
                }
            }
        });
    </script>
</body>
</html>
