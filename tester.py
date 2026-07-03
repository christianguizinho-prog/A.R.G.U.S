"""
Tester - Verifica se A.R.G.U.S. está funcionando corretamente
Executar: python tester.py
"""

import sys
import importlib
import os
from datetime import datetime


class Tester:
    def __init__(self):
        self.results = []
        self.timestamp = datetime.now()
    
    def print_header(self):
        print("""
        ╔════════════════════════════════════════════╗
        ║     A.R.G.U.S. v3.0 - SYSTEM TESTER       ║
        ╚════════════════════════════════════════════╝
        """)
    
    def test_python_version(self):
        """Testa versão do Python"""
        print("[1/8] Verificando Python...")
        version = sys.version_info
        if version.major >= 3 and version.minor >= 8:
            print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
            self.results.append(("Python Version", True))
            return True
        else:
            print(f"✗ Python 3.8+ necessário (encontrado {version.major}.{version.minor})")
            self.results.append(("Python Version", False))
            return False
    
    def test_module(self, name, import_name=None):
        """Testa se um módulo está instalado"""
        if import_name is None:
            import_name = name
        
        try:
            importlib.import_module(import_name)
            print(f"✓ {name}")
            return True
        except ImportError:
            print(f"✗ {name} não encontrado")
            return False
    
    def test_dependencies(self):
        """Testa todas as dependências"""
        print("\n[2/8] Testando dependências...")
        results = []
        
        modules = [
            ("CustomTkinter", "customtkinter"),
            ("psutil", "psutil"),
            ("matplotlib", "matplotlib"),
            ("requests", "requests"),
            ("OpenCV", "cv2"),
            ("Pillow", "PIL"),
            ("pandas", "pandas"),
            ("openpyxl", "openpyxl"),
            ("speedtest-cli", "speedtest"),
        ]
        
        for name, import_name in modules:
            results.append(self.test_module(name, import_name))
        
        self.results.append(("Dependencies", all(results)))
        return all(results)
    
    def test_directories(self):
        """Testa se diretórios necessários existem"""
        print("\n[3/8] Verificando diretórios...")
        dirs = ['assets', 'database']
        results = []
        
        for dir_name in dirs:
            if os.path.exists(dir_name):
                print(f"✓ Diretório '{dir_name}' existe")
                results.append(True)
            else:
                print(f"⚠️ Diretório '{dir_name}' não encontrado (será criado)")
                os.makedirs(dir_name, exist_ok=True)
                results.append(True)
        
        self.results.append(("Directories", all(results)))
        return all(results)
    
    def test_modules(self):
        """Testa se módulos do projeto funcionam"""
        print("\n[4/8] Testando módulos do projeto...")
        results = []
        
        modules_to_test = [
            "config",
            "monitor",
            "network",
            "ai",
            "database",
            "graphs",
        ]
        
        for module_name in modules_to_test:
            try:
                __import__(module_name)
                print(f"✓ {module_name}.py")
                results.append(True)
            except Exception as e:
                print(f"✗ {module_name}.py - {str(e)[:50]}")
                results.append(False)
        
        self.results.append(("Project Modules", all(results)))
        return all(results)
    
    def test_monitor(self):
        """Testa monitoramento do sistema"""
        print("\n[5/8] Testando monitor do sistema...")
        try:
            from monitor import monitor
            stats = monitor.get_all_stats()
            
            print(f"✓ CPU: {stats['cpu']:.1f}%")
            print(f"✓ RAM: {stats['ram']:.1f}%")
            print(f"✓ GPU: {stats['gpu']:.1f}%")
            print(f"✓ Temperatura: {stats['temperature']:.1f}°C")
            print(f"✓ Processos: {stats['processes']}")
            
            self.results.append(("System Monitor", True))
            return True
        except Exception as e:
            print(f"✗ Erro ao monitorar: {e}")
            self.results.append(("System Monitor", False))
            return False
    
    def test_network(self):
        """Testa informações de rede"""
        print("\n[6/8] Testando rede...")
        try:
            from network import network
            net_info = network.get_all_network_info()
            
            print(f"✓ IP: {net_info['public_ip']}")
            print(f"✓ Localização: {net_info['city']}, {net_info['country']}")
            print(f"✓ Status: {'Online' if net_info['is_online'] else 'Offline'}")
            
            self.results.append(("Network", True))
            return True
        except Exception as e:
            print(f"✗ Erro na rede: {e}")
            self.results.append(("Network", False))
            return False
    
    def test_database(self):
        """Testa banco de dados"""
        print("\n[7/8] Testando banco de dados...")
        try:
            from database import db
            
            # Tentar log
            db.log_system_stats(45.0, 60.0, 30.0, 55.0, 56.0, 0, 0, 198)
            print("✓ Log de sistema gravado")
            
            db.log_alert('TEST', 'Teste de alerta', 'NORMAL')
            print("✓ Alerta gravado")
            
            stats = db.get_latest_stats(limit=1)
            print(f"✓ Recuperados {len(stats)} registros")
            
            self.results.append(("Database", True))
            return True
        except Exception as e:
            print(f"✗ Erro no banco: {e}")
            self.results.append(("Database", False))
            return False
    
    def test_ai(self):
        """Testa IA"""
        print("\n[8/8] Testando IA...")
        try:
            from ai import ai
            
            greeting = ai.get_greeting()
            print(f"✓ Saudação: {greeting[:50]}...")
            
            response = ai.get_response("Olá")
            print(f"✓ Resposta: {response[:50]}...")
            
            self.results.append(("AI Module", True))
            return True
        except Exception as e:
            print(f"✗ Erro na IA: {e}")
            self.results.append(("AI Module", False))
            return False
    
    def print_summary(self):
        """Imprime resumo dos testes"""
        print("\n" + "="*46)
        print("RESUMO DOS TESTES")
        print("="*46)
        
        passed = 0
        failed = 0
        
        for test_name, result in self.results:
            status = "✓ PASSOU" if result else "✗ FALHOU"
            print(f"{status:12} - {test_name}")
            if result:
                passed += 1
            else:
                failed += 1
        
        print("="*46)
        print(f"Total: {passed} passados, {failed} falhados")
        
        if failed == 0:
            print("\n🎉 Todos os testes passaram! A.R.G.U.S. está pronto!")
        else:
            print(f"\n⚠️ {failed} teste(s) falharam. Verifique os erros acima.")
        
        print("="*46)
    
    def run(self):
        """Executa todos os testes"""
        self.print_header()
        
        self.test_python_version()
        self.test_dependencies()
        self.test_directories()
        self.test_modules()
        self.test_monitor()
        self.test_network()
        self.test_database()
        self.test_ai()
        
        self.print_summary()
        
        # Retornar True se todos passaram
        return all(result for _, result in self.results)


if __name__ == "__main__":
    tester = Tester()
    success = tester.run()
    sys.exit(0 if success else 1)
