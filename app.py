import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px
import os


# ======================
# LANGUE (TOUJOURS EN PREMIER)
# ======================
lang = st.sidebar.selectbox("🌐 Language / Langue", ["Français", "English"])


# =======================
# TEXTES (UN SEUL DICTIONNAIRE)
# =======================
texts = {
    "Français": {
        "title": "🌍 Dashboard Chercheurs Africains",
        "about": "📖 Présentation",
        "description": """
Cette plateforme permet de visualiser la mobilité des chercheurs africains à travers le monde.

Vous pouvez explorer :
- les pays d'origine et d'accueil
- les disciplines
- l'évolution dans le temps

Les données peuvent être filtrées.
        """,
        "origin": "Pays d'origine",
        "destination": "Pays d'accueil",
        "all": "Tous",
        "table": "Tableau des données",
        "evolution": "Évolution annuelle",
        "country": "Pays d'accueil",
        "discipline": "Disciplines",
        "total": "Total chercheurs",
        "countries": "Nombre de pays",
        "disc": "Disciplines",
        "form": "📝 Ajouter un chercheur",
        "first": "Prénom",
        "last": "Nom",
        "origin_f": "Pays d'origine",
        "dest_f": "Pays d'accueil",
        "inst": "Institution",
        "year": "Année",
        "add": "Ajouter",
        "success": "Ajout réussi ✅"
    },
    "English": {
        "title": "🌍 African Researchers Dashboard",
        "about": "📖 About",
        "description": """
This platform allows you to explore the mobility of African researchers worldwide.

You can analyze:
- origin and host countries
- disciplines
- trends over time

Data can be filtered.
        """,
        "origin": "Origin country",
        "destination": "Host country",
        "all": "All",
        "table": "Data table",
        "evolution": "Yearly evolution",
        "country": "Host countries",
        "discipline": "Disciplines",
        "total": "Total researchers",
        "countries": "Number of countries",
        "disc": "Disciplines",
        "form": "📝 Add researcher",
        "first": "First Name",
        "last": "Last Name",
        "origin_f": "Origin Country",
        "dest_f": "Host Country",
        "inst": "Institution",
        "year": "Year",
        "add": "Add",
        "success": "Added successfully ✅"
    }
}


# =======================
# INTRODUCTION
# =======================
st.title(texts[lang]["title"])

st.markdown(f"""
### {texts[lang]["about"]}

{texts[lang]["description"]}
""")

st.markdown("---")


# ======================
# LANGUE
# ======================
#lang = st.sidebar.selectbox("🌐 Language / Langue", ["Français", "English"])

#texts = {
    #"Français": {
        #"title": "🌍 Dashboard Chercheurs Africain",
        #"origin": "Pays d'origine",
        #"destination": "Pays d'accueil",
        #"all": "Tous",
        #"table": "Tableau des données",
        #"evolution": "Évolution annuelle",
        #"country": "Pays d'accueil",
        #"discipline": "Disciplines",
        #"total": "Total chercheurs",
        #"countries": "Nombre de pays",
        #"disc": "Disciplines",
        #"form": "📝 Ajouter un chercheur",
        #"first": "Prénom",
        #"last": "Nom",
        #"origin_f": "Pays d'origine",
        #"dest_f": "Pays d'accueil",
        #"inst": "Institution",
        #"year": "Année",
        #"add": "Ajouter",
        #"success": "Ajout réussi ✅"
    #},
    #"English": {
        #"title": "🌍 African Researchers Dashboard",
        #"origin": "Origin country",
        #"destination": "Host country",
        #"all": "All",
        #"table": "Data table",
        #"evolution": "Yearly evolution",
        #"country": "Host countries",
        #"discipline": "Disciplines",
        #"total": "Total researchers",
        #"countries": "Number of countries",
        #"disc": "Disciplines",
        #"form": "📝 Add researcher",
        #"first": "First Name",
        #"last": "Last Name",
        #"origin_f": "Origin Country",
        #"dest_f": "Host Country",
        #"inst": "Institution",
        #"year": "Year",
        #"add": "Add",
       # "success": "Added successfully ✅"
    #}
#}



# ======================
# LOGIN SYSTEM
# ======================
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

def login():
    st.subheader("🔐 Connexion admin" if lang=="Français" else "🔐 Admin login")

    username = st.text_input("Utilisateur" if lang=="Français" else "Username")
    password = st.text_input("Mot de passe" if lang=="Français" else "Password", type="password")

    if st.button("Se connecter" if lang=="Français" else "Login"):
        if username == "TsafackThereseFowanMichel-Pharel" and password == "TsafackT@FoMi-Pha":
            st.session_state["logged_in"] = True
            st.success("Connexion réussie")
        else:
            st.error("Identifiants incorrects")

st.set_page_config(layout="wide")

# ======================
# CONNECTION
# ======================
#@st.cache_resource
#def get_conn():
    #return psycopg2.connect(os.environ["DATABASE_URL"])


@st.cache_resource
def get_conn():

    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        st.error("DATABASE_URL not found")
        st.stop()

    return psycopg2.connect(database_url)
#def get_conn():
    #return psycopg2.connect(
        #"postgresql://postgres.gmpepshnxwdzdjfzhsgk:TsafackThereseFowanMichelPharel@aws-1-eu-north-1.pooler.supabase.com:6543/postgres"
    #)
#def get_conn():
    #return psycopg2.connect(
        #os.getenv("DATABASE_URL")
    #)


# ======================
# LOAD DATA
# ======================
@st.cache_data
def load_data():
    try:
        conn = get_conn()
        df = pd.read_sql("SELECT * FROM africa_researchers;", conn)

        if df.empty:
            return df

        df = df.sort_values(by="id")
        return df

    except Exception as e:
        st.error(f"Erreur base de données : {e}")
        return pd.DataFrame()
df = load_data()

#@st.cache_data
#def load_data():
    #conn = get_conn()
    #conn.rollback()  # 🔥 important
    #df = df.sort_values(by="id")

    #df = pd.read_sql("SELECT * FROM africa_researchers;", conn)
    #df["year"] = pd.to_numeric(df["year"], errors="coerce")
    #df = df.dropna(subset=["year"])
    #df["year"] = df["year"].astype(int)
    #return df
#df = load_data()

#@st.cache_data
#def load_data():
    #conn = get_conn()
    #df = pd.read_sql("SELECT * FROM africa_researchers;", conn)

    #df = df.sort_values(by="id")

    #df["year"] = pd.to_numeric(df["year"], errors="coerce")
    #df = df.dropna(subset=["year"])
    #df["year"] = df["year"].astype(int)

    #return df

#df = load_data()

# ======================
# TRADUCTION COLONNES
# ======================
columns_translation = {
    "Français": {
        "id": "ID",
        "first_name": "Prénom",
        "last_name": "Nom",
        "country_origin": "Pays d'origine",
        "country_current": "Pays d'accueil",
        "institution": "Institution",
        "discipline": "Discipline",
        "year": "Année"
    },
    "English": {
        "id": "ID",
        "first_name": "First Name",
        "last_name": "Last Name",
        "country_origin": "Origin Country",
        "country_current": "Host Country",
        "institution": "Institution",
        "discipline": "Discipline",
        "year": "Year"
    }
}

# ======================
# TITLE
# ======================
#st.title(texts[lang]["title"])

# ======================
# FILTERS
# ======================
origin = st.sidebar.selectbox(
    texts[lang]["origin"],
    [texts[lang]["all"]] + sorted(df["country_origin"].unique())
)

destination = st.sidebar.selectbox(
    texts[lang]["destination"],
    [texts[lang]["all"]] + sorted(df["country_current"].unique())
)

df_filtered = df.copy()

if origin != texts[lang]["all"]:
    df_filtered = df_filtered[df_filtered["country_origin"] == origin]

if destination != texts[lang]["all"]:
    df_filtered = df_filtered[df_filtered["country_current"] == destination]

# ======================
# METRICS
# ======================
col1, col2, col3 = st.columns(3)

col1.metric(texts[lang]["total"], int(len(df_filtered)))
col2.metric(texts[lang]["countries"], int(df_filtered["country_origin"].nunique()))
col3.metric(texts[lang]["disc"], int(df_filtered["discipline"].nunique()))

# ======================
# TABLE (TRADUITE)
# ======================
#st.subheader(texts[lang]["table"])

#df_display = df_filtered.rename(columns=columns_translation[lang])

#st.dataframe(df_display, use_container_width=True, hide_index=True)
#
# ======================
# TABLE (EMAIL MASQUÉ)
# ======================
st.subheader(texts[lang]["table"])
df_display = df_filtered.rename(columns=columns_translation[lang])

df_table = df_display.copy()

# masquer email si présent
if "email" in df_table.columns:
    df_table = df_table.drop(columns=["email"], errors="ignore")
    #df_table["email"] = df_table["email"].apply(
        #lambda x: "XXXXXXXX" if pd.notna(x) and str(x).strip() != "" else ""
    #)

st.dataframe(df_table, use_container_width=True, hide_index=True)

# ======================
# EVOLUTION (ANNÉES FIXES)
# ======================

df_year = df_filtered.groupby("year").size().reset_index(name="total")

fig1 = px.line(df_year, x="year", y="total", markers=True,
               title=texts[lang]["evolution"],labels={
        "year": texts[lang]["year"],
        "total": texts[lang]["total"]
    })

fig1.update_layout(
    xaxis=dict(type='category'),  # 🔥 FIX CRUCIAL
    yaxis=dict(dtick=1)
)

st.plotly_chart(fig1, use_container_width=True)

# ======================
# COUNTRY
# ======================

df_country = df_filtered.groupby("country_current").size().reset_index(name="total")

fig2 = px.bar(
    df_country,
    x="country_current",
    y="total",
    title=texts[lang]["country"],
    labels={
        "country_current": texts[lang]["country"],
        "total": texts[lang]["total"]
    }
)

fig2.update_yaxes(tickmode="linear", dtick=1, tickformat=",d")

st.plotly_chart(fig2, use_container_width=True)

#df_country = df_filtered.groupby("country_current").size().reset_index(name="total")

#fig2 = px.bar(df_country, x="country_current", y="total",
              #title=texts[lang]["country"])

#fig2.update_yaxes(tickmode="linear", dtick=1, tickformat=",d")

#st.plotly_chart(fig2, use_container_width=True)

# ======================
# DISCIPLINE
# ======================
df_disc = df_filtered.groupby("discipline").size().reset_index(name="total")

fig3 = px.bar(df_disc, x="discipline", y="total",
              title=texts[lang]["discipline"])

fig3.update_yaxes(tickmode="linear", dtick=1, tickformat=",d")

st.plotly_chart(fig3, use_container_width=True)

# ======================
# FORMULAIRE
# ======================
import datetime
import os

st.subheader(texts[lang]["form"])

with st.form("form_unique"):

    col1, col2 = st.columns(2)

    with col1:
        first_name = st.text_input(texts[lang]["first"])
        last_name = st.text_input(texts[lang]["last"])
        country_origin = st.text_input(texts[lang]["origin_f"])

    with col2:
        country_current = st.text_input(texts[lang]["dest_f"])
        institution = st.text_input(texts[lang]["inst"])
        discipline = st.text_input("Discipline")
        year = st.number_input(texts[lang]["year"], 1900, 2100, step=1)

    # 📧 EMAIL (OPTIONNEL)
    email = st.text_input(
        "Adresse email (optionel) " if lang=="Français" else "Email adress (optional)"
    )

    submitted = st.form_submit_button(texts[lang]["add"])

    if submitted:

        # ======================
        # INSERT SQL (SANS EMAIL)
        # ======================
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO africa_researchers
            (first_name, last_name, country_origin, country_current, institution, discipline, year)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (first_name, last_name, country_origin, country_current, institution, discipline, year))

        conn.commit()
        cur.close()

        # ======================
        # STOCKAGE EMAIL CSV
        # ======================
        if email.strip() != "":

            now = datetime.datetime.now()

            # dossier sécurisé
            os.makedirs("secure_data", exist_ok=True)

            filename = f"secure_data/emails_{now.year}_{now.month:02d}.csv"

            file_exists = os.path.isfile(filename)

            df_email = pd.DataFrame([{
                "email": email,
                "date": now.strftime("%Y-%m-%d %H:%M:%S")
            }])

            df_email.to_csv(
                filename,
                mode="a",
                header=not file_exists,
                index=False
            )

        st.success(texts[lang]["success"])
        st.cache_data.clear()




# ======================
# 🌍 CARTE MONDIALE
# ======================
st.subheader("🌍 Carte des chercheurs" if lang=="Français" else "🌍 World map")

df_map = df_filtered.groupby("country_current").size().reset_index(name="total")

fig_map = px.scatter_geo(
    df_map,
    locations="country_current",
    locationmode="country names",
    size="total",
    hover_name="country_current",
    projection="natural earth",
    title="Répartition mondiale" if lang=="Français" else "Global distribution"
)

fig_map.update_layout(
    geo=dict(showframe=False, showcoastlines=True),
)

st.plotly_chart(fig_map, use_container_width=True)

# ======================
# 🔁 SANKEY MIGRATION
# ======================
st.subheader("🔁 Flux de migration" if lang=="Français" else "🔁 Migration flow")

df_sankey = (
    df_filtered.groupby(["country_origin", "country_current"])
    .size()
    .reset_index(name="value")
)

# créer liste unique des pays
labels = list(pd.concat([df_sankey["country_origin"], df_sankey["country_current"]]).unique())

# mapping index
label_index = {label: i for i, label in enumerate(labels)}

# source / target
source = df_sankey["country_origin"].map(label_index)
target = df_sankey["country_current"].map(label_index)
value = df_sankey["value"]

import plotly.graph_objects as go

fig_sankey = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        label=labels
    ),
    link=dict(
        source=source,
        target=target,
        value=value
    )
)])

fig_sankey.update_layout(
    title_text="Flux Origine → Destination" if lang=="Français"
               else "Origin → Destination Flow"
)

st.plotly_chart(fig_sankey, use_container_width=True)

#Espace admin


# ======================
# 🔐 ZONE ADMIN (EXPORT + LOGOUT)
# ======================
st.markdown("---")

if st.session_state.get("logged_in", False):

    colA, colB = st.columns([3,1])

    with colA:
        st.subheader("🔐 Admin")

    with colB:
        if st.button("🚪 Déconnexion" if lang=="Français" else "🚪 Logout"):
            st.session_state["logged_in"] = False
            st.rerun()

    # EXPORT CSV
    csv = df_filtered.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Télécharger CSV" if lang=="Français" else "📥 Download CSV",
        data=csv,
        file_name="researchers.csv",
        mime="text/csv"
    )

    # EXPORT PDF
    try:
        from reportlab.platypus import SimpleDocTemplate, Table

        def create_pdf(dataframe):
            file = "data.pdf"
            doc = SimpleDocTemplate(file)
            table_data = [dataframe.columns.tolist()] + dataframe.values.tolist()
            doc.build([Table(table_data)])
            return file

        if st.button("📄 Générer PDF" if lang=="Français" else "📄 Generate PDF"):

            pdf_file = create_pdf(df_filtered)

            with open(pdf_file, "rb") as f:
                st.download_button(
                    "⬇️ Télécharger PDF" if lang=="Français" else "⬇️ Download PDF",
                    f,
                    file_name="researchers.pdf"
                )

    except:
        st.warning("PDF non disponible")

else:
    login()
#Espace admin
#st.markdown("---")

#st.subheader("🔐 Espace administrateur" if lang=="Français" else "🔐 Admin area")

#admin_password = st.text_input(
    #"Mot de passe admin" if lang=="Français" else "Admin password",
    #type="password"
#)

#if admin_password == "TsafackT@FoMi@Pha":  # 🔥 change ce mot de passe

    #st.success("Accès autorisé")

    # ======================
    # EXPORT CSV
    # ======================
    #csv = df_filtered.to_csv(index=False).encode("utf-8")

    #st.download_button(
        #label="📥 Télécharger CSV" if lang=="Français" else "📥 Download CSV",
        #data=csv,
        #file_name="researchers.csv",
        #mime="text/csv"
    #)

    # ======================
    # EXPORT PDF
    # ======================
    #from reportlab.platypus import SimpleDocTemplate, Table

    #def create_pdf(dataframe):
        #file = "data.pdf"
        #doc = SimpleDocTemplate(file)

        #table_data = [dataframe.columns.tolist()] + dataframe.values.tolist()
        #table = Table(table_data)

        #doc.build([table])
        #return file

    #if st.button("📄 Télécharger PDF" if lang=="Français" else "📄 Download PDF"):

        #pdf_file = create_pdf(df_filtered)

        #with open(pdf_file, "rb") as f:
            #st.download_button(
                #"⬇️ Télécharger PDF" if lang=="Français" else "⬇️ Download PDF",
                #f,
                #file_name="researchers.pdf"
            #)

#else:
    #st.info("Accès restreint" if lang=="Français" else "Restricted access")


