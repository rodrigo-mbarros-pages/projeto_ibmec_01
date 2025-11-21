from pathlib import Path

# Este arquivo está em: <projeto>/src/config.py
# BASE_DIR = raiz do projeto (PROJETO_IBMEC_01)
BASE_DIR = Path(__file__).resolve().parent.parent

# Diretório de código-fonte
SRC_DIR = BASE_DIR / "src"

# Diretórios principais na raiz
ARTIFACTS_DIR = BASE_DIR / "artifacts"
LOGS_DIR = BASE_DIR / "logs"
TESTS_DIR = BASE_DIR / "tests"

# Subpastas específicas
DATA_DIR = SRC_DIR / "data"              # onde está o schemas.py
MODELS_DIR = ARTIFACTS_DIR / "models"    # modelos treinados / artefatos

# API
API_TITLE = "API_VALDESC_CUPOM"          # corrigi o typo AOU_TITLE
API_VERSION = "1.0.0"
API_DESCRIPTION = "API para validar cupons de desconto"
