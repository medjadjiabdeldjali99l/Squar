from playwright.sync_api import sync_playwright
import streamlit as st
import pandas as pd


def excel_fnc_change(header,values,lis,devis):
    if ( header == "Dinar algérien"):
        for i in range(len(lis)):
            if devis == lis[i]:
                achat = lis[i+1]
        values = [i/float(achat) for i in values]
        return values         
    elif devis == "Dinar algérien" :
        for i in range(len(lis)):
            if header == lis[i]:
                vente = lis[i+2]
        values = [i*float(vente) for i in values]
        return values
    else :

        b=False
        c=False
        for i in range(len(lis)):
            if header == lis[i]:
                vente = lis[i+2]
                b=True
        for i in range(len(lis)):
            if devis == lis[i]:
                achat = lis[i+1]
                c=True
        if b and c :
            values=[(i*float(vente))/float(achat) for i in values]
        return values


def scrap():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)  # Utilisation de Firefox en mode headless
        page = browser.new_page()
        
        # Accéder à la page des taux de change
        page.goto('http://www.forexalgerie.com/')
        
        # Attendre que la page se charge complètement
        page.wait_for_selector('td')
        
        # Récupérer les éléments contenant les taux de change
        td_elements = page.query_selector_all('td')
        
        # Extraire le texte des éléments
        l = [element.inner_text() for element in td_elements if element.inner_text().strip()]
        
        l = [i for i in l if i != "" and not i.strip().startswith(("+", "-"))]
        headers = l[:3]
        rows = l[3:]
        table_data = [rows[i:i + 3] for i in range(0, len(rows), 3)]
        df = pd.DataFrame(table_data, columns=headers)
        
        # Sauvegarder dans un fichier CSV
        df.to_csv("output1.csv", index=False, encoding="utf-8")
        
        # Fermer le navigateur
        browser.close()
    
    return l, df



st.set_page_config(layout="wide")

# Titre de l'application
st.title("Convertisseur de devises")
st.markdown("Convertissez facilement vos devises avec une interface conviviale.")

col1, col2 = st.columns([1, 1])

with col1:

    montant = st.number_input("Entrez un montant :", min_value=0.0, step=0.01)

    # Sélection de la devise
    devise = st.selectbox(
        "Sélectionnez une devise :",
        ["Dinar algérien","Euro", "Dollar US", "Dollar Canadien", "Livre Sterling", 
         "Franc Suisse", "Livre Turque", "Yuan Chinois", 
         "Rial Saoudien", "Dirham Emirati", "Dinar Tunisien", "Dirham Marocain"]
    )

    devis_change = st.selectbox(
        "Dans quelle devise souhaitez-vous convertir votre argent ? :",
        ["Dinar algérien","Euro", "Dollar US", "Dollar Canadien", "Livre Sterling", 
         "Franc Suisse", "Livre Turque", "Yuan Chinois", 
         "Rial Saoudien", "Dirham Emirati", "Dinar Tunisien", "Dirham Marocain"]
    )
    
    if st.button("Soumettre"):
        if (devise==devis_change):
            st.write(f"Vous avez entré : {montant} dans la devise {devise} et vous souhaitez le convertir en la devise {devis_change}Le montant que vous recevrez {montant}")
        else:
            # Affichage des résultats
            st.write(f"Vous avez entré : {montant} dans la devise {devise} et vous souhaitez le convertir en la devise {devis_change}")
            (lis,df)=scrap()
            r=[]
            if devise=="Dinar algérien" :
                for i in range( len(lis)):
                    if devis_change==lis[i]:
                        resultat_direct=float(montant)/float(lis[i+1])
                st.write(f"Vous avez entré : {montant} dans la devise {devise} et vous souhaitez le convertir en la devise {devis_change} Le montant que vous recevrez {resultat_direct}")
            elif devis_change=="Dinar algérien":
                for i in range ( len ( lis)):
                    if devise==lis[i]:
                        resultat_direct=float(montant)*float(lis[i+2])
                st.write(f"Vous avez entré : {montant} dans la devise {devise} et vous souhaitez le convertir en la devise {devis_change} Le montant que vous recevrez {resultat_direct}")
            else:

                for i in range(len(lis)):
                    if lis[i]==devise:
                        r.append(montant)
                        r.append(lis[i+2])

                for i in range(len(lis)):
                    if lis[i]==devis_change:
                        r.append(lis[i+1])

                finale = round((float(r[0]) * float(r[1])) / float(r[2]), 2)

                st.write(f"Vous avez entré : {montant} dans la devise {devise} et vous souhaitez le convertir en la devise {devis_change} Le montant que vous recevrez {finale}")

            
            st.table(df.style.hide(axis="index"))
            st.write(df.style.hide(axis="index"))
            st.markdown("Merci pour votre confiance 🎈")






with col2:
    uploaded_file = st.file_uploader("Sinon Envoyez un fichier Excel", type=["xlsx", "xls"])

    devis_change_excel = st.selectbox(
        "Dans quelle devise souhaitez-vous convertir votre fichier excel? :",
        ["Dinar algérien","Euro", "Dollar US", "Dollar Canadien", "Livre Sterling", 
         "Franc Suisse", "Livre Turque", "Yuan Chinois", 
         "Rial Saoudien", "Dirham Emirati", "Dinar Tunisien", "Dirham Marocain"]
    )

    fichh = st.text_input("Veuillez saisir le nom du nouveau fichier :")

    if st.button("Soumettre file"):
        if uploaded_file is not None:
            try:
                # Lire le fichier Excel
                dff = pd.read_excel(uploaded_file)
                
                # Afficher un message de succès
                st.success("Fichier reçu et chargé avec succès!")
                
                # Afficher les données dans un tableau interactif
                st.dataframe(dff)
                
                # Télécharger les données traitées (facultatif)

                header = dff.columns[0]  # Le premier élément de la première colonne
                values = dff.iloc[0:, 0].tolist()  # Toutes les autres lignes dans la même colonne
                
                
                if header == devis_change_excel:
                    st.write(f"Vous avez entré le fichier dans la devise {header} et vous souhaitez le convertir en la devise {devis_change_excel} Le fichier que vous recevrez ne change pas ")
                else:
                    (lis,df)=scrap()
                    resultat_excel_change=excel_fnc_change(header,values,lis,devis_change_excel)

                    
                    dff[devis_change_excel]=resultat_excel_change

                    st.dataframe(dff)

                    if fichh:
                        output_file = f"{fichh}.xlsx"
                        dff.to_excel(output_file, index=False, engine='openpyxl')


                    csv_data = dff.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Télécharger les données en CSV",
                        data=csv_data,
                        file_name="donnees_converties.csv",
                        mime="text/csv",
                    )
            except Exception as e:
                    st.error(f"Erreur lors de la lecture du fichier: {e}")
            st.markdown("Merci pour votre confiance 🎈")


    

st.markdown("<hr>", unsafe_allow_html=True)
