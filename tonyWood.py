import pandas as pd
from pandasql import sqldf

def get_winner(result, home_team, away_team):
    try:
        # Split del risultato per ottenere i gol
        goals = result.split("–")  # Attenzione: il carattere potrebbe essere un trattino speciale
        home_goals = int(goals[0].strip())
        away_goals = int(goals[1].strip())

        # Determinare il vincitore
        if home_goals > away_goals:
            return home_team
        elif away_goals > home_goals:
            return away_team
        else:
            return "Pareggio"
    except Exception as e:
        return None  # Se il valore non = valido, restituisce None
    
# Funzione per eseguire query SQL su Pandas
def run_query(query, title):
    return sqldf(f"SELECT '{title}' AS type, * FROM ({query})", {"df": df})

# Funzione per eseguire query SQL e restituire il conteggio
def run_query_count(query, title):
    return sqldf(f"SELECT '{title}' AS type, COUNT(*) AS count FROM ({query})", {"df": df})

# Funzione per ottenere il conteggio totale dei record
def get_total_count():
    return sqldf("SELECT COUNT(*) AS total_count FROM df", {"df": df})

if __name__ == "__main__":
    
    columns_to_cast_float = [
        "selectorQuota1Media",
        "selectorQuotaxMedia",
        "selectorQuota2Media",
        "selectorQuotaOver25Media",
        "selectorQuotaUnder25Media",
        "selectorQuotaGoalMedia",
        "selectorQuotaNoGoalMedia"
        ]
    
    # Caricare il CSV
    df = pd.read_csv("C:/Users/chris/Desktop/tonyWoodScript/scrapingRisultati.csv", delimiter=",")
    df[columns_to_cast_float] = df[columns_to_cast_float].apply(pd.to_numeric, errors="coerce")
    df["risultatoFinale"] = df.apply(lambda row: get_winner(row["selectorRisultato"], row["squadraCasa"], row["squadraOspite"]), axis=1)

    # Definire le query con titoli
    queries = {
        "Minima tra 1X2 = 1": """
            SELECT * FROM df 
            WHERE 
                CASE 
                    WHEN selectorQuota1Media <= selectorQuotaxMedia 
                     AND selectorQuota1Media <= selectorQuota2Media 
                    THEN 1 ELSE 0 
                END = 1
        """,
        "Minima tra 1X2 = 2": """
            SELECT * FROM df 
            WHERE 
                CASE 
                    WHEN selectorQuota2Media <= selectorQuotaxMedia 
                     AND selectorQuota2Media <= selectorQuota1Media 
                    THEN 1 ELSE 0 
                END = 1
        """,
        "Massima tra 1X2 = 1": """
            SELECT * FROM df 
            WHERE 
                CASE 
                    WHEN selectorQuota1Media >= selectorQuotaxMedia 
                     AND selectorQuota1Media >= selectorQuota2Media 
                    THEN 1 ELSE 0 
                END = 1
        """,
        "Massima tra 1X2 = 2": """
            SELECT * FROM df 
            WHERE 
                CASE 
                    WHEN selectorQuota2Media >= selectorQuotaxMedia 
                     AND selectorQuota2Media >= selectorQuota1Media 
                    THEN 1 ELSE 0 
                END = 1
        """,
        "Massima tra 1X2 = X": """
            SELECT * FROM df 
            WHERE 
                CASE 
                    WHEN selectorQuotaxMedia >= selectorQuota1Media 
                     AND selectorQuotaxMedia >= selectorQuota2Media 
                    THEN 1 ELSE 0 
                END = 1
        """,
        "Quota X tra 4 e 5, vittoria della favorita": """
            SELECT * FROM df 
            WHERE selectorQuotaxMedia BETWEEN 4 AND 5 
            AND ((selectorQuota1Media < selectorQuota2Media AND risultatoFinale = squadraCasa) 
            OR (selectorQuota2Media < selectorQuota1Media AND risultatoFinale = squadraOspite))
        """,
        "Quota X tra 4 e 5, vittoria della sfavorita": """
            SELECT * FROM df 
            WHERE selectorQuotaxMedia BETWEEN 4 AND 5 
            AND ((selectorQuota1Media > selectorQuota2Media AND risultatoFinale = squadraCasa) 
            OR (selectorQuota2Media > selectorQuota1Media AND risultatoFinale = squadraOspite))
        """,
        "Quota Goal e Under < No Goal e Over": """
            SELECT * FROM df 
            WHERE selectorQuotaGoalMedia < selectorQuotaNoGoalMedia
            AND selectorQuotaGoalMedia < selectorQuotaOver25Media 
            AND selectorQuotaUnder25Media < selectorQuotaNoGoalMedia
            AND selectorQuotaUnder25Media < selectorQuotaOver25Media
        """,
        "Quota Over < Goal": """
            SELECT * FROM df 
            WHERE selectorQuotaOver25Media < selectorQuotaGoalMedia
        """,
        "Quota No Goal e Over < Goal e Under": """
            SELECT * FROM df 
            WHERE selectorQuotaNoGoalMedia < selectorQuotaGoalMedia
            AND selectorQuotaNoGoalMedia < selectorQuotaUnder25Media 
            AND selectorQuotaOver25Media < selectorQuotaGoalMedia
            AND selectorQuotaOver25Media < selectorQuotaUnder25Media
        """,
        "Under e No Goal < 2, Goal e Over >= 2": """
            SELECT * FROM df 
            WHERE selectorQuotaUnder25Media < 2 
            AND selectorQuotaNoGoalMedia < 2 
            AND selectorQuotaGoalMedia >= 2 
            AND selectorQuotaOver25Media >= 2
            AND selectorQuotaUnder25Media < selectorQuotaGoalMedia
            AND selectorQuotaUnder25Media < selectorQuotaOver25Media
            AND selectorQuotaNoGoalMedia < selectorQuotaGoalMedia
            AND selectorQuotaNoGoalMedia < selectorQuotaOver25Media
        """,
        "Goal < Over e No Goal, Under > Over": """
            SELECT * FROM df 
            WHERE selectorQuotaGoalMedia < selectorQuotaOver25Media 
            AND selectorQuotaNoGoalMedia > selectorQuotaOver25Media 
            AND selectorQuotaUnder25Media > selectorQuotaOver25Media
        """
    }

    # Eseguire tutte le query e salvarle in un dizionario
    results = {title: run_query(query, title) for title, query in queries.items()}

    # Unire tutti i risultati in un unico DataFrame
    final_result = pd.concat(results.values(), ignore_index=True)

    # Eseguire tutte le query e salvarle in un dizionario per il conteggio
    count_results = {title: run_query_count(query, title) for title, query in queries.items()}

    # Unire tutti i risultati in un unico DataFrame per il conteggio
    count_final_result = pd.concat(count_results.values(), ignore_index=True)

    # Ottenere il conteggio totale dei record
    total_count = get_total_count()

    # Aggiungere il conteggio totale ai risultati
    count_final_result['total_count'] = total_count['total_count'][0]

    # Stampare i risultati
    print(count_final_result)

    # Salvare i risultati in CSV
    final_result.to_csv("risultati_query.csv", index=False)
    count_final_result.to_csv("conteggio_query_con_totale.csv", index=False)
