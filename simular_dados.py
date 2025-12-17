import pandas as pd
import numpy as np

np.random.seed(42)

# numero de registros a serem gerados
n = 40

# simulação dos dados
dados = pd.DataFrame({
    "Idade": np.random.randint(18, 46, n),
    "Horas_IA_Dia": np.round(np.random.uniform(0.5, 6.0, n), 1),
    "Frequencia_Semanal": np.random.randint(1, 8, n),
    "Sexo": np.random.choice(["Masculino", "Feminino"], n),
    "Nivel_Experiencia": np.random.choice(
        ["Estudante", "Júnior", "Pleno", "Sênior"],
        n,
        p=[0.4, 0.25, 0.2, 0.15]  # distribuição mais realista para o nível de senioridade
    )
})


dados.to_csv("dados_pesquisa_ia.csv", index=False, encoding="utf-8")

print("Arquivo 'dados_pesquisa_ia.csv' gerado com sucesso!")
