import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix

# ==========================================
# 1. Preparação dos Dados e Ambiente
# ==========================================
def load_and_prep_data():
    iris = load_iris()
    X, y = iris.data, iris.target
    
    # Divisão 70% treino, 30% teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
    
    # Normalização
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    return X_train_scaled, X_test_scaled, y_train, y_test

# Discretização dos estados contínuos para a Tabela Q
def discretize_state(state, bins):
    state_discrete = []
    for i in range(len(state)):
        # np.digitize retorna o índice do bin. Subtraímos 1 para usar como índice zero-based
        state_discrete.append(np.digitize(state[i], bins[i]) - 1)
    return tuple(state_discrete)

# ==========================================
# 2. Agente Q-Learning
# ==========================================
class RLAgent:
    def __init__(self, n_actions, state_shape, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.n_actions = n_actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        # Tabela Q: Dimensões = formato do estado + número de ações
        self.q_table = np.zeros(state_shape + (n_actions,))
        
    def choose_action(self, state):
        if np.random.uniform(0, 1) < self.epsilon:
            return np.random.choice(self.n_actions) # Exploração
        else:
            return np.argmax(self.q_table[state])   # Explotação

    def learn(self, state, action, reward):
        # Como a classificação de 1 amostra é um episódio completo (1 passo),
        # não há próximo estado (s'). Portanto, max Q(s', a') é 0.
        target = reward 
        self.q_table[state][action] = self.q_table[state][action] + \
            self.alpha * (target - self.q_table[state][action])

# ==========================================
# 3 e 4. Treinamento, Teste e Rodadas
# ==========================================
def run_experiments(n_runs=30, n_episodes=1000):
    X_train, X_test, y_train, y_test = load_and_prep_data()
    
    # Definindo limites dos bins para discretização (-3 a 3 devido ao StandardScaler)
    n_bins = 5
    bins = [np.linspace(-3, 3, n_bins) for _ in range(X_train.shape[1])]
    state_shape = tuple([n_bins + 1] * X_train.shape[1])
    
    accuracies = []
    all_confusion_matrices = []
    learning_curves = []
    
    for run in range(n_runs):
        agent = RLAgent(n_actions=3, state_shape=state_shape, alpha=0.1, epsilon=0.2)
        rewards_history = []
        
        # Treinamento
        for ep in range(n_episodes):
            # Amostra aleatória do treino
            idx = np.random.randint(0, len(X_train))
            raw_state = X_train[idx]
            true_class = y_train[idx]
            
            state = discretize_state(raw_state, bins)
            action = agent.choose_action(state)
            
            # Recompensa
            reward = 1 if action == true_class else -1
            
            agent.learn(state, action, reward)
            rewards_history.append(reward)
            
        # Avaliação a cada 100 episódios para curva de aprendizado
        window = 50
        moving_avg = np.convolve(rewards_history, np.ones(window)/window, mode='valid')
        learning_curves.append(moving_avg)
        
        # Teste
        y_pred = []
        for i in range(len(X_test)):
            state = discretize_state(X_test[i], bins)
            # No teste, epsilon é 0 (apenas explotação)
            action = np.argmax(agent.q_table[state])
            y_pred.append(action)
            
        acc = accuracy_score(y_test, y_pred)
        accuracies.append(acc)
        all_confusion_matrices.append(confusion_matrix(y_test, y_pred))
        
    return accuracies, all_confusion_matrices, learning_curves, bins

# ==========================================
# 5. Execução e Geração de Gráficos
# ==========================================
accuracies, cms, learning_curves, bins = run_experiments(n_runs=30, n_episodes=1000)

mean_acc = np.mean(accuracies)
std_acc = np.std(accuracies)
mean_cm = np.mean(cms, axis=0)

print(f"--- Resultados de 30 Rodadas ---")
print(f"Acurácia Média: {mean_acc * 100:.2f}%")
print(f"Desvio Padrão: {std_acc * 100:.2f}%")

# Gráficos
plt.figure(figsize=(12, 5))

# Gráfico 1: Curva de Aprendizado
plt.subplot(1, 2, 1)
mean_learning_curve = np.mean(learning_curves, axis=0)
plt.plot(mean_learning_curve, color='blue')
plt.title('Curva de Aprendizado (Média de 30 runs)')
plt.xlabel('Episódios de Treinamento')
plt.ylabel('Recompensa Média (Janela Móvel)')
plt.grid(True)

# Gráfico 2: Matriz de Confusão Média
plt.subplot(1, 2, 2)
sns.heatmap(mean_cm, annot=True, fmt='.1f', cmap='Blues', 
            xticklabels=['Setosa', 'Versicolor', 'Virginica'], 
            yticklabels=['Setosa', 'Versicolor', 'Virginica'])
plt.title('Matriz de Confusão Média')
plt.xlabel('Predição (Ação do Agente)')
plt.ylabel('Classe Verdadeira')

plt.tight_layout()
plt.savefig('graficos.png')
print("\nGráficos salvos como 'graficos.png'")
# plt.show() 