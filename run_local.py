"""
Script para executar a aplicação localmente
"""
import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """Instala dependências"""
    print("📦 Instalando dependências...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependências instaladas com sucesso!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False
    return True

def check_env_file():
    """Verifica se arquivo .env existe"""
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️ Arquivo .env não encontrado!")
        print("📝 Criando arquivo .env baseado no exemplo...")
        
        # Copiar arquivo de exemplo
        try:
            with open("env_example.txt", "r") as example:
                content = example.read()
            
            with open(".env", "w") as env_file:
                env_file.write(content)
            
            print("✅ Arquivo .env criado!")
            print("🔧 IMPORTANTE: Edite o arquivo .env com suas credenciais reais")
            return False
        except Exception as e:
            print(f"❌ Erro ao criar .env: {e}")
            return False
    
    return True

def check_credentials():
    """Verifica se credenciais existem"""
    credentials_file = Path("credentials.json")
    if not credentials_file.exists():
        print("⚠️ Arquivo credentials.json não encontrado!")
        print("📝 Você precisa:")
        print("   1. Criar service account no Google Cloud")
        print("   2. Baixar arquivo JSON das credenciais")
        print("   3. Salvar como 'credentials.json' na raiz do projeto")
        return False
    
    return True

def run_streamlit():
    """Executa a aplicação Streamlit"""
    print("🚀 Iniciando aplicação Streamlit...")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Aplicação encerrada pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao executar Streamlit: {e}")

def main():
    """Função principal"""
    print("🏠 Sistema de Controle de Perdas - Setup Local")
    print("=" * 50)
    
    # Verificar Python
    python_version = sys.version_info
    if python_version < (3, 9):
        print(f"❌ Python {python_version.major}.{python_version.minor} não suportado")
        print("✅ Use Python 3.9 ou superior")
        return
    
    print(f"✅ Python {python_version.major}.{python_version.minor} OK")
    
    # Instalar dependências
    if not install_requirements():
        return
    
    # Verificar arquivo .env
    env_ready = check_env_file()
    
    # Verificar credenciais
    cred_ready = check_credentials()
    
    if not env_ready or not cred_ready:
        print("\n⚠️ CONFIGURAÇÃO NECESSÁRIA:")
        print("1. Configure suas credenciais no arquivo .env")
        print("2. Adicione o arquivo credentials.json do Google")
        print("3. Execute este script novamente")
        return
    
    print("\n✅ Todas as verificações passaram!")
    print("🚀 Iniciando aplicação...")
    print("📱 A aplicação será aberta em: http://localhost:8501")
    print("🛑 Use Ctrl+C para parar")
    
    # Executar Streamlit
    run_streamlit()

if __name__ == "__main__":
    main()
