"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel


def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """
    import os
    import zipfile
    import pandas as pd
    import glob
    
    # Create output directory if it doesn't exist
    os.makedirs("files/output", exist_ok=True)
    
    # Initialize lists to store data from all files
    all_data = []
    
    # Process all zip files in the input directory
    zip_files = glob.glob("files/input/*.csv.zip")
    zip_files.sort()  # Ensure consistent order
    
    for zip_file in zip_files:
        with zipfile.ZipFile(zip_file, 'r') as z:
            # Get the first (and likely only) CSV file in the zip
            csv_name = z.namelist()[0]
            with z.open(csv_name) as f:
                df = pd.read_csv(f)
                all_data.append(df)
    
    # Combine all data
    combined_df = pd.concat(all_data, ignore_index=True)
    
    # Remove the 'Unnamed: 0' column if it exists (index column)
    if 'Unnamed: 0' in combined_df.columns:
        combined_df = combined_df.drop('Unnamed: 0', axis=1)
    
    # Create client_id as the index
    combined_df['client_id'] = combined_df.index
    
    # ========== CLIENT.CSV ==========
    client_df = combined_df[['client_id', 'age', 'job', 'marital', 'education', 'credit_default', 'mortgage']].copy()
    
    # Clean job field: change "." to "" and "-" to "_"
    client_df['job'] = client_df['job'].str.replace('.', '', regex=False)
    client_df['job'] = client_df['job'].str.replace('-', '_', regex=False)
    
    # Clean education field: change "." to "_" and "unknown" to pd.NA
    client_df['education'] = client_df['education'].str.replace('.', '_', regex=False)
    client_df['education'] = client_df['education'].replace('unknown', pd.NA)
    
    # Convert credit_default: "yes" to 1, everything else to 0
    client_df['credit_default'] = (client_df['credit_default'] == 'yes').astype(int)
    
    # Convert mortgage: "yes" to 1, everything else to 0
    client_df['mortgage'] = (client_df['mortgage'] == 'yes').astype(int)
    
    # ========== CAMPAIGN.CSV ==========
    campaign_df = combined_df[['client_id', 'number_contacts', 'contact_duration', 
                              'previous_campaign_contacts', 'previous_outcome', 
                              'campaign_outcome', 'day', 'month']].copy()
    
    # Convert previous_outcome: "success" to 1, everything else to 0
    campaign_df['previous_outcome'] = (campaign_df['previous_outcome'] == 'success').astype(int)
    
    # Convert campaign_outcome: "yes" to 1, everything else to 0
    campaign_df['campaign_outcome'] = (campaign_df['campaign_outcome'] == 'yes').astype(int)
    
    # Create last_contact_date with format "YYYY-MM-DD" using 2022 as year
    campaign_df['last_contact_date'] = pd.to_datetime(
        campaign_df['day'].astype(str) + '-' + 
        campaign_df['month'].astype(str) + '-2022', 
        format='%d-%b-%Y'
    ).dt.strftime('%Y-%m-%d')
    
    # Drop the original day and month columns
    campaign_df = campaign_df.drop(['day', 'month'], axis=1)
    
    # ========== ECONOMICS.CSV ==========
    economics_df = combined_df[['client_id', 'cons_price_idx', 'euribor_three_months']].copy()
    
    # Save all files
    client_df.to_csv("files/output/client.csv", index=False)
    campaign_df.to_csv("files/output/campaign.csv", index=False)
    economics_df.to_csv("files/output/economics.csv", index=False)
    
    return


if __name__ == "__main__":
    clean_campaign_data()
