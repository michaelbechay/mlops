import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Fonction pour générer des marches aléatoires et calculer le fair price
def simulate_random_walks(start_date, end_date, num_simulations, mean, std_dev, last_price, risk_free_rate):
    num_days = (end_date - start_date).days
    date_range = pd.date_range(start=start_date, end=end_date, freq='B')  # 'B' pour les jours ouvrés
    final_prices = []
    random_walks = np.zeros((len(date_range), num_simulations))
    random_walks[0] = last_price

    for i in range(1, len(date_range)):
        random_walks[i] = random_walks[i - 1] * np.exp((mean - 0.5 * std_dev**2) + std_dev * np.random.normal(size=num_simulations))

    final_prices = random_walks[-1]
    fair_price = np.mean(final_prices) * np.exp(-risk_free_rate * (num_days / 365))

    return date_range, random_walks, fair_price

# Demandez à l'utilisateur d'entrer les paramètres requis
while True:
    start_date_input = "2000-01-01"
    try:
        start_date = pd.to_datetime(start_date_input)
        break  # Sortie de la boucle si la conversion est réussie
    except ValueError:
        print("La date entrée est invalide. Veuillez entrer une date au format YYYY-MM-DD.")

while True:
    try:
        risk_free_rate_input = "0.05"
        risk_free_rate = float(risk_free_rate_input)
        break  # Sortie de la boucle si la conversion est réussie
    except ValueError:
        print("Le taux d'intérêt entré est invalide. Veuillez entrer un nombre décimal (par exemple, 0.05 pour 5%).")

# Téléchargez les données AAPL
aapl_data = yf.download('AAPL', start='2020-01-01')

# Estimer les paramètres
aapl_sub_period = aapl_data['Close']['2020-01-01':'2020-02-28']
daily_returns = aapl_sub_period.pct_change().dropna()
mean = daily_returns.mean()
std_dev = daily_returns.std()

# Assurez-vous que la date de début est un jour de trading
if start_date not in aapl_data.index:
    nearest_index = aapl_data.index.searchsorted(start_date)
    # Gérer le cas où la date est après la dernière date disponible
    if nearest_index >= len(aapl_data.index):
        nearest_index = len(aapl_data.index) - 1
    start_date = aapl_data.index[nearest_index]

# Générer les marches aléatoires
last_price = aapl_data['Close'].loc[start_date]
end_date = aapl_data.index[-1]  # Dernière date des données historiques
date_range, random_walks, fair_price = simulate_random_walks(start_date, end_date, 100, mean, std_dev, last_price, risk_free_rate)

# Afficher les résultats
plt.figure(figsize=(14, 7))
plt.plot(aapl_data['Close'], label='Prix Historiques')
for i in range(random_walks.shape[1]):
    plt.plot(date_range, random_walks[:, i], 'k-', lw=0.3, alpha=0.2)
plt.title('Prix Historiques vs. 100 Marches Aléatoires pour AAPL')
plt.xlabel('Date')
plt.ylabel('Prix des Actions')
plt.legend()
plt.show()

print(f"Fair price estimé de l'action Apple: {fair_price:.2f}")
