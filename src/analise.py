from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
IMG_DIR = BASE_DIR / "images"
IMG_DIR.mkdir(exist_ok=True)

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 20)


def carregar_csv(nome_arquivo):
    df = pd.read_csv(DATA_DIR / nome_arquivo, sep=None, engine="python")
    df.columns = df.columns.str.strip().str.upper()
    df["SALARY"] = pd.to_numeric(df["SALARY"], errors="coerce")
    return df


def medidas(serie):
    
    return {
        "Quantidade": int(serie.count()),
        "Média": round(serie.mean(), 2),
        "Mediana": round(serie.median(), 2),
        "Mínimo": serie.min(),
        "Máximo": serie.max(),
        "Desvio padrão": round(serie.std(), 2),
    }


def resumo_por_grupo(df, coluna):
  
    return (
        df.groupby(coluna)["SALARY"]
        .agg(["count", "mean", "median", "min", "max"])
        .round(2)
        .sort_values("mean", ascending=False)
    )


def titulo(texto):
    print("\n" + "=" * 70)
    print(texto)
    print("=" * 70)

df1 = carregar_csv("query_01.csv")
df2 = carregar_csv("query_02.csv")

titulo("QUERY 1 - Visão geral")
print("Dimensões (linhas, colunas):", df1.shape)
print("\nPrimeiras linhas:")
print(df1.head())
print("\nTipos de dados:")
print(df1.dtypes)
print("\nValores nulos por coluna:")
print(df1.isnull().sum())
print("\nLinhas duplicadas:", df1.duplicated().sum())

titulo("QUERY 1 - Medidas estatísticas do salário")
stats1 = medidas(df1["SALARY"])
for chave, valor in stats1.items():
    print(f"{chave}: {valor}")

dif = stats1["Média"] - stats1["Mediana"]
print(f"\nDiferença média - mediana: {dif:.2f}")
if dif > 0:
    print("Média acima da mediana -> distribuição assimétrica à direita "
          "(poucos salários muito altos puxam a média para cima).")
else:
    print("Média próxima ou abaixo da mediana -> distribuição mais simétrica.")

titulo("QUERY 1 - Salário por departamento")
por_depto = resumo_por_grupo(df1, "DEPARTMENT_NAME")
print(por_depto)

titulo("QUERY 1 - Salário por cargo")
por_cargo = resumo_por_grupo(df1, "JOB_TITLE")
print(por_cargo)

titulo("QUERY 2 - Visão geral")
print("Dimensões (linhas, colunas):", df2.shape)
print("\nPrimeiras linhas:")
print(df2.head())
print("\nValores nulos por coluna:")
print(df2.isnull().sum())

titulo("QUERY 2 - Medidas estatísticas do salário")
stats2 = medidas(df2["SALARY"])
for chave, valor in stats2.items():
    print(f"{chave}: {valor}")

titulo("QUERY 2 - Funcionários por região")
por_regiao = resumo_por_grupo(df2, "REGION_NAME")
print(por_regiao)

titulo("QUERY 2 - Funcionários por país")
por_pais = resumo_por_grupo(df2, "COUNTRY_NAME")
print(por_pais)

titulo("QUERY 2 - Funcionários por cidade")
por_cidade = resumo_por_grupo(df2, "CITY")
print(por_cidade)

fig, ax = plt.subplots(figsize=(9, 5))
ax.hist(df1["SALARY"].dropna(), bins=15, color="#4C78A8", edgecolor="white")
ax.axvline(stats1["Média"], color="red", linestyle="--", label=f"Média: {stats1['Média']:.0f}")
ax.axvline(stats1["Mediana"], color="green", linestyle="-", label=f"Mediana: {stats1['Mediana']:.0f}")
ax.set_title("Distribuição dos salários dos funcionários")
ax.set_xlabel("Salário")
ax.set_ylabel("Quantidade de funcionários")
ax.legend()
fig.tight_layout()
fig.savefig(IMG_DIR / "histograma_salarios.png", dpi=150)
plt.close(fig)


ordem = (
    df1.groupby("DEPARTMENT_NAME")["SALARY"].median().sort_values().index.tolist()
)
dados_box = [df1.loc[df1["DEPARTMENT_NAME"] == d, "SALARY"].dropna() for d in ordem]
fig, ax = plt.subplots(figsize=(10, 6))
ax.boxplot(dados_box, vert=False, tick_labels=ordem)
ax.set_title("Salários por departamento (ordenado pela mediana)")
ax.set_xlabel("Salário")
fig.tight_layout()
fig.savefig(IMG_DIR / "boxplot_salarios_departamento.png", dpi=150)
plt.close(fig)


fig, ax = plt.subplots(figsize=(8, 5))
medias_regiao = por_regiao["mean"].sort_values(ascending=False)
ax.bar(medias_regiao.index, medias_regiao.values, color="#F58518")
ax.set_title("Salário médio por região")
ax.set_ylabel("Salário médio")
for i, v in enumerate(medias_regiao.values):
    ax.text(i, v, f"{v:,.0f}", ha="center", va="bottom")
fig.tight_layout()
fig.savefig(IMG_DIR / "barras_salario_medio_regiao.png", dpi=150)
plt.close(fig)


fig, ax = plt.subplots(figsize=(8, 5))
qtd_regiao = por_regiao["count"].sort_values(ascending=False)
ax.bar(qtd_regiao.index, qtd_regiao.values, color="#54A24B")
ax.set_title("Quantidade de funcionários por região")
ax.set_ylabel("Funcionários")
for i, v in enumerate(qtd_regiao.values):
    ax.text(i, v, str(int(v)), ha="center", va="bottom")
fig.tight_layout()
fig.savefig(IMG_DIR / "barras_funcionarios_regiao.png", dpi=150)
plt.close(fig)

titulo("Concluído")
print(f"Gráficos salvos em: {IMG_DIR}")
