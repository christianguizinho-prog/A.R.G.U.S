"""
IA Conversacional - A.R.G.U.S.
"""

import random
from datetime import datetime


class AI:
    def __init__(self, user_name="Usuário"):
        self.user_name = user_name
        self.conversation_history = []
        self.system_status = "NORMAL"

    def set_system_status(self, status, message=""):
        """Define o status do sistema"""
        self.system_status = status
        self.last_status_message = message

    def get_greeting(self):
        """Retorna uma saudação personalizada"""
        hour = datetime.now().hour
        
        if hour < 12:
            period = "bom dia"
        elif hour < 18:
            period = "boa tarde"
        else:
            period = "boa noite"
        
        greetings = [
            f"Olá {self.user_name}. {period.capitalize()}! Todos os sistemas estão operacionais.",
            f"{period.capitalize()}, {self.user_name}. Estou aqui para monitorar seu sistema.",
            f"Bem-vindo de volta, {self.user_name}. {period.capitalize()}!",
            f"{period.capitalize()}! Como posso ajudá-lo hoje, {self.user_name}?",
        ]
        
        return random.choice(greetings)

    def analyze_system(self, stats):
        """
        Analisa o sistema e gera insights
        stats: dicionário com todas as informações do sistema
        """
        cpu = stats.get('cpu', 0)
        ram = stats.get('ram', 0)
        disk = stats.get('disk', 0)
        temp = stats.get('temperature', 0)
        
        messages = []
        
        # Análise de CPU
        if cpu > 80:
            messages.append(f"⚠️ CPU está em {cpu:.1f}%. Alto uso detectado!")
        elif cpu > 50:
            messages.append(f"CPU operando em {cpu:.1f}%. Normal.")
        else:
            messages.append(f"✓ CPU em {cpu:.1f}%. Excelente!")
        
        # Análise de RAM
        if ram > 85:
            messages.append(f"⚠️ Memória crítica em {ram:.1f}%!")
        elif ram > 70:
            messages.append(f"RAM em {ram:.1f}%. Considere liberar memória.")
        else:
            messages.append(f"✓ Memória em {ram:.1f}%. Ótimo!")
        
        # Análise de Temperatura
        if temp > 75:
            messages.append(f"🔥 Temperatura em {temp:.1f}°C. Sistema aquecido!")
        elif temp > 60:
            messages.append(f"Temperatura em {temp:.1f}°C. Normal.")
        else:
            messages.append(f"✓ Temperatura em {temp:.1f}°C. Fresco!")
        
        # Análise de Disco
        if disk > 90:
            messages.append(f"⚠️ Disco quase cheio: {disk:.1f}%!")
        elif disk > 75:
            messages.append(f"Disco em {disk:.1f}%. Considere liberar espaço.")
        else:
            messages.append(f"✓ Disco em {disk:.1f}%. Espaço suficiente.")
        
        return " ".join(messages)

    def get_status_message(self):
        """Retorna mensagem sobre o status geral"""
        if self.system_status == "NORMAL":
            messages = [
                "Nenhuma atividade suspeita detectada.",
                "Sistema operando normalmente.",
                "Tudo em ordem. Continuarei monitorando.",
                "Sem problemas no momento. Estou vigilante.",
            ]
        elif self.system_status == "WARNING":
            messages = [
                "Detectei algumas anomalias. Fique atento.",
                "Há alertas para revisar.",
                "Alguns parâmetros estão acima do normal.",
                "Recomendo analisar os alertas recentes.",
            ]
        elif self.system_status == "CRITICAL":
            messages = [
                "⚠️ ALERTA CRÍTICO! Ação imediata recomendada!",
                "🚨 Sistema em estado crítico!",
                "Situação grave detectada. Intervenção necessária!",
                "⚠️ Status crítico! Verifique os alertas agora!",
            ]
        else:
            messages = ["Status desconhecido."]
        
        return random.choice(messages)

    def get_tip(self):
        """Retorna uma dica útil"""
        tips = [
            "💡 Dica: Limpe o cache regularmente para melhorar o desempenho.",
            "💡 Dica: Atualize seus drivers para otimizar a performance.",
            "💡 Dica: Feche abas do navegador desnecessárias para liberar RAM.",
            "💡 Dica: Faça backup regularmente de seus arquivos importantes.",
            "💡 Dica: Use SSD para armazenamento e maior velocidade.",
            "💡 Dica: Monitore processos em background que consomem recursos.",
            "💡 Dica: Mantenha sua casa de software atualizada e segura.",
        ]
        return random.choice(tips)

    def get_response(self, user_input):
        """Gera uma resposta baseada na entrada do usuário"""
        user_input_lower = user_input.lower()
        
        # Respostas específicas
        if any(word in user_input_lower for word in ['oi', 'olá', 'opa', 'e aí']):
            return f"Olá {self.user_name}! Tudo bem?"
        
        elif any(word in user_input_lower for word in ['status', 'como está', 'tudo bem']):
            return self.get_status_message()
        
        elif any(word in user_input_lower for word in ['dica', 'sugestão', 'conselho']):
            return self.get_tip()
        
        elif any(word in user_input_lower for word in ['obrigado', 'valeu', 'thanks']):
            return "De nada! Sempre à disposição!"
        
        elif any(word in user_input_lower for word in ['adeus', 'tchau', 'até logo']):
            return "Até logo! Continuarei monitorando seu sistema."
        
        elif any(word in user_input_lower for word in ['quem é você', 'o que você é', 'qual seu nome']):
            return "Sou A.R.G.U.S., seu assistente de monitoramento em tempo real. Aqui para proteger seu sistema!"
        
        else:
            responses = [
                f"Entendo, {self.user_name}. Estou sempre monitorando.",
                "Anotado! Continuarei acompanhando o sistema.",
                "Certo! Deixa comigo.",
                "Interessante observação. Vou ficar atento.",
                "Recebi. Estou aqui para ajudar!",
            ]
            return random.choice(responses)

    def add_to_history(self, user_msg, ai_msg):
        """Adiciona à histórico de conversa"""
        self.conversation_history.append({
            'timestamp': datetime.now(),
            'user': user_msg,
            'ai': ai_msg
        })


# Instância global
ai = AI()
