$paths = @(
    "app\api",
    "app\agents",
    "app\parser",
    "app\ocr",
    "app\chunking",
    "app\embeddings",
    "app\vectorstore",
    "app\services",
    "app\prompts",
    "app\database",
    "app\models",
    "app\schemas",
    "app\utils",
    "app\config"
)

foreach ($path in $paths) {
    New-Item -ItemType Directory -Path $path -Force | Out-Null
}

New-Item -ItemType File -Path "app\main.py" -Force | Out-Null