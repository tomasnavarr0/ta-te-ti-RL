# Usa una imagen base con Python y pipenv
FROM mcr.microsoft.com/vscode/devcontainers/python:3.12

# Instala dependencias adicionales
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && apt-get clean -y

# Instala pipenv globalmente
RUN pip install --upgrade pip && \
    pip install pipenv

# Configura el entorno de trabajo
WORKDIR /workspace

# Copia el Pipfile y Pipfile.lock (si existen) al contenedor
COPY Pipfile Pipfile.lock* ./

# Instala las dependencias del proyecto usando pipenv
RUN if [ -f Pipfile ]; then pipenv install --dev; fi

# Instala pre-commit globalmente
RUN pip install pre-commit

# Copia el archivo de configuración de pre-commit al contenedor
COPY .pre-commit-config.yaml ./
