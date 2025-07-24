import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# DB setup
engine = create_engine('sqlite:///clients.db')
Base = declarative_base()

class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    nom = Column(String(100))
    prenom = Column(String(100))
    email = Column(String(100))
    troubles = Column(Text)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Streamlit UI
st.title("Logiciel de gestion de clients")

menu = st.sidebar.selectbox("Menu", ["Ajouter un client", "Voir les clients", "Supprimer un client"])

if menu == "Ajouter un client":
    st.header("Ajouter un nouveau client")
    nom = st.text_input("Nom")
    prenom = st.text_input("Prénom")
    email = st.text_input("Email")
    troubles = st.text_area("Troubles / Notes")

    if st.button("Enregistrer"):
        nouveau_client = Client(nom=nom, prenom=prenom, email=email, troubles=troubles)
        session.add(nouveau_client)
        session.commit()
        st.success("Client ajouté avec succès !")

elif menu == "Voir les clients":
    st.header("Liste des clients")
    clients = session.query(Client).all()
    if not clients:
        st.info("Aucun client trouvé.")
    else:
        data = [{
            "ID": c.id,
            "Nom": c.nom,
            "Prénom": c.prenom,
            "Email": c.email,
            "Troubles": c.troubles
        } for c in clients]
        df = pd.DataFrame(data)
        st.dataframe(df)

elif menu == "Supprimer un client":
    st.header("Supprimer un client")
    ids = [str(c.id) + " - " + c.nom for c in session.query(Client).all()]
    choix = st.selectbox("Choisir le client à supprimer", ids)

    if st.button("Supprimer"):
        id_to_delete = int(choix.split(" - ")[0])
        client = session.query(Client).filter_by(id=id_to_delete).first()
        if client:
            session.delete(client)
            session.commit()
            st.success("Client supprimé.")
