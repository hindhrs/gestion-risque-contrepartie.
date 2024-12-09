import streamlit as st
from web3 import Web3


# Connect to Polygon RPC
w3 = Web3(Web3.HTTPProvider('HTTP://127.0.0.1:7545'))
if w3.isConnected():
    print("Connected")
else:
    print("Failed to connect")


# Load smart contract
contract_address = "0x985BDdDA7E299dAffb2A372448B6dd9632e1B341"
abi = [
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_portefeuille",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "_scoreCredit",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_limiteExposition",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "_collaterale",
				"type": "uint256"
			}
		],
		"name": "ajouterContrepartie",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "contrepartie",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "limiteExposition",
				"type": "uint256"
			}
		],
		"name": "ContrepartieAjoutee",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_portefeuille",
				"type": "address"
			}
		],
		"name": "desactiverContrepartie",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "contrepartie",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "nouvelleExposition",
				"type": "uint256"
			}
		],
		"name": "ExpositionMiseAJour",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "contrepartie",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "exposition",
				"type": "uint256"
			}
		],
		"name": "LimiteDepassee",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_portefeuille",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "_nouvelleExposition",
				"type": "uint256"
			},
			{
				"internalType": "bool",
				"name": "estLongue",
				"type": "bool"
			}
		],
		"name": "mettreAJourExposition",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_portefeuille",
				"type": "address"
			}
		],
		"name": "calculerRatioCouverture",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_portefeuille",
				"type": "address"
			}
		],
		"name": "calculerRisque",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "contreparties",
		"outputs": [
			{
				"internalType": "address",
				"name": "portefeuille",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "scoreCredit",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "limiteExposition",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "expositionLongue",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "expositionCourte",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "expositionCourante",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "collaterale",
				"type": "uint256"
			},
			{
				"internalType": "bool",
				"name": "estActif",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "expositions",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]

contract = w3.eth.contract(address=contract_address, abi=abi)

# Streamlit App Title
st.title("Gestionnaire de Risque Contrepartie")

# User Wallet Connection
st.sidebar.header("Connexion au portefeuille")
user_wallet = st.sidebar.text_input("Adresse du portefeuille", "")

if st.sidebar.button("Connecter"):
    if Web3.isAddress(user_wallet):
        st.sidebar.success(f"Connecté au portefeuille : {user_wallet}")
    else:
        st.sidebar.error("Adresse invalide. Veuillez réessayer.")

# Tab Selection
selected_tab = st.sidebar.radio("Menu", [
    "Ajouter une contrepartie",
    "Mettre à jour l'exposition",
    "Calculer le risque",
    "Calculer le ratio de couverture",
    "Désactiver une contrepartie"
])

# Add Counterparty
if selected_tab == "Ajouter une contrepartie":
    st.header("Ajouter une Contrepartie")
    portefeuille = st.text_input("Adresse de la contrepartie")
    score_credit = st.number_input("Score de crédit", min_value=0, value=100)
    limite_exposition = st.number_input("Limite d'exposition", min_value=0)
    collaterale = st.number_input("Montant collatéral", min_value=0)

    if st.button("Ajouter"):
        if Web3.isAddress(portefeuille):
            try:
                tx_hash = contract.functions.ajouterContrepartie(
                    portefeuille,
                    score_credit,
                    limite_exposition,
                    collaterale
                ).transact({'from': '0xE33912d6Ab42d5c6F444e18b9987656F0eC370F2', 'gas': 3000000})
                
                receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
                st.success(f"Transaction successful! Hash: {receipt.transactionHash.hex()}")
            except Exception as e:
                st.error(f"Erreur lors de l'ajout de la contrepartie : {e}")
        else:
            st.error("Adresse invalide.")

# Update Exposure
elif selected_tab == "Mettre à jour l'exposition":
    st.header("Mettre à jour l'exposition")
    portefeuille = st.text_input("Adresse de la contrepartie")
    exposition = st.number_input("Nouvelle exposition", min_value=0)
    est_longue = st.radio("Type d'exposition", ["Longue", "Courte"])

    if st.button("Mettre à jour"):
        if Web3.isAddress(portefeuille):
            try:
                tx_hash = contract.functions.mettreAJourExposition(
                    portefeuille,
                    exposition,
                    est_longue == "Longue"
                ).transact({'from': '0xE33912d6Ab42d5c6F444e18b9987656F0eC370F2', 'gas': 3000000})
                
                receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
                st.success(f"Exposition mise à jour avec succès ! Transaction Hash: {receipt.transactionHash.hex()}")
            except Exception as e:
                st.error(f"Erreur lors de la mise à jour de l'exposition : {e}")
        else:
            st.error("Adresse invalide.")


# Calculate Risk
elif selected_tab == "Calculer le risque":
    st.header("Calculer le Risque")
    portefeuille = st.text_input("Adresse de la contrepartie", help="Saisissez l'adresse Ethereum de la contrepartie.")

    if st.button("Calculer"):
        if not Web3.isAddress(portefeuille):
            st.error("Adresse de portefeuille invalide. Veuillez saisir une adresse Ethereum valide.")
        else:
            try:
                # Retrieve counterparty details
                contrepartie = contract.functions.contreparties(portefeuille).call()

                # Check if the counterparty exists
                if contrepartie[0] == "0x0000000000000000000000000000000000000000":
                    st.error(f"La contrepartie {portefeuille} n'existe pas. Veuillez l'ajouter.")
                elif not contrepartie[7]:  # contrepartie.estActif (index 7)
                    st.warning(f"La contrepartie {portefeuille} est désactivée.")
                else:
                    risque = contract.functions.calculerRisque(portefeuille).call()
                    st.success(f"Risque calculé: {risque}")
            except Exception as e:
                st.error("Une erreur est survenue lors du calcul du risque.")
                st.error(f"Détails : {str(e)}")
   


# Calculate Coverage Ratio
elif selected_tab == "Calculer le ratio de couverture":
    st.header("Calculer le Ratio de Couverture")
    portefeuille = st.text_input("Adresse de la contrepartie")

    if st.button("Calculer Ratio"):
        if Web3.isAddress(portefeuille):
            try:
                ratio = contract.functions.calculerRatioCouverture(portefeuille).call()
                st.write(f"Ratio de couverture: {ratio}%")
            except Exception as e:
                st.error(f"Erreur lors du calcul du ratio de couverture : {e}")
        else:
            st.error("Adresse invalide.")

# Deactivate Counterparty
elif selected_tab == "Désactiver une contrepartie":
    st.header("Désactiver une Contrepartie")
    portefeuille = st.text_input("Adresse de la contrepartie")

    if st.button("Désactiver"):
        if Web3.isAddress(portefeuille):
            try:
                tx_hash = contract.functions.desactiverContrepartie(portefeuille).transact({'from': '0xE33912d6Ab42d5c6F444e18b9987656F0eC370F2', 'gas': 3000000})
                
                receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
                st.success(f"Contrepartie désactivée avec succès ! Transaction Hash: {receipt.transactionHash.hex()}")
            except Exception as e:
                st.error(f"Erreur lors de la désactivation de la contrepartie : {e}")
        else:
            st.error("Adresse invalide.")

balance = w3.eth.get_balance('0xE33912d6Ab42d5c6F444e18b9987656F0eC370F2')
print("Wallet balance:", w3.fromWei(balance, 'ether'))

