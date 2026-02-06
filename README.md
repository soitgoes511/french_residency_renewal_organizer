# French Residence Permit Renewal Tracker 🇫🇷

<p align="center">
  <img src="app/static/icon.svg" alt="App Icon" width="128" height="128">
</p>

<p align="center">
  <strong>Track your French residence permit renewal with confidence</strong>
</p>

<p align="center">
  <em>Suivez votre demande de titre de séjour en toute sérénité</em>
</p>

---

A web application designed to help foreign residents in France navigate the complex process of renewing a **Titre de Séjour** or applying for a **Carte de Résident de Longue Durée-UE** (10-year residence card).

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎯 **Two Permit Types** | Titre de Séjour renewal or Carte de Résident (10-year) |
| 📋 **Complete Checklists** | All required documents with French names & English translations |
| 🔗 **Official Links** | Direct links to service-public.gouv.fr for each document |
| 📊 **Progress Tracking** | Visual percentage indicator shows your completion status |
| 💾 **Persistent Storage** | SQLite database saves your progress across restarts |
| 🐳 **Containerized** | Runs locally via Podman or Docker |
| 🌙 **Modern Dark UI** | Clean, responsive design with French-themed accents |

## 📸 Screenshot

The application features a modern dark theme with:
- Intuitive permit type selector
- Progress bar with real-time updates
- Categorized document checklist
- Links to official government resources

## 🚀 Quick Start

### Prerequisites

- [Podman](https://podman.io/) or [Docker](https://www.docker.com/)

### Using Podman (Recommended)

```bash
# Clone the repository
git clone https://github.com/soitgoes511/french_residency_renewal_organizer.git
cd french_residency_renewal_organizer

# Build the image
podman build -t residence-permit-tracker .

# Create data directory for persistence
mkdir -p data

# Run the container
podman run -d --name residence-tracker -p 5000:5000 -v "${PWD}/data:/app/data" residence-permit-tracker

# Open in browser
# http://localhost:5000
```

### Using Docker Compose

```bash
docker-compose up --build
# Access at http://localhost:5000
```

### Container Management

```bash
# Stop the container
podman stop residence-tracker

# Start again (data persists!)
podman start residence-tracker

# View logs
podman logs residence-tracker

# Remove container
podman rm residence-tracker
```

## 📝 Usage

1. **Select Your Permit Type**
   - **Titre de Séjour** - For renewing your current residence permit (1-4 years)
   - **Carte de Résident** - For applying for a 10-year card (after 5 years in France)

2. **Track Your Documents**
   - Each document shows the French name and English translation
   - Click to mark documents as complete
   - Use the links to access official sources

3. **Monitor Progress**
   - Watch your completion percentage grow
   - All progress is saved automatically

## 📄 Document Requirements

### Carte de Résident de Longue Durée-UE (10-Year Card)

Based on [service-public.gouv.fr/F17359](https://www.service-public.fr/particuliers/vosdroits/F17359):

- Valid passport
- Full birth certificate (apostilled for foreign-born)
- Proof of address (less than 6 months)
- Proof of regular residence (5 years)
- Proof of resources (5 years)
- Health insurance certificate
- **French B1 level certificate** (required as of 2025)
- **Civic exam certificate** (required as of 2026)
- Republican principles commitment
- Tax stamp (€225)

### Titre de Séjour (Renewal)

- Valid passport & current permit
- Proof of address (less than 3 months)
- Proof of resources (last 3 pay slips)
- Tax notice
- Health insurance certificate
- Republican principles commitment
- Tax stamp (€225)

## 🔗 Important Links

| Resource | URL |
|----------|-----|
| 📝 ANEF Portal | https://administration-etrangers-en-france.interieur.gouv.fr/ |
| 📖 Service-Public | https://www.service-public.fr/particuliers/vosdroits/N110 |
| 💳 Tax Stamp | https://timbres.impots.gouv.fr/ |
| 🏥 Ameli | https://www.ameli.fr/ |
| 🗣️ French Tests | https://www.service-public.fr/particuliers/vosdroits/F34501 |

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | Python 3.11 + Flask |
| Frontend | Vanilla HTML/CSS/JavaScript |
| Database | SQLite3 |
| Container | Podman / Docker |

## 📁 Project Structure

```
french_residency_renewal_organizer/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
├── app/
│   ├── app.py              # Flask REST API
│   ├── database.py         # SQLite operations
│   ├── documents.py        # Document definitions
│   └── static/
│       ├── index.html      # Main SPA page
│       ├── styles.css      # Dark theme styling
│       ├── app.js          # Frontend logic
│       └── icon.svg        # App icon
└── data/
    └── residence.db        # SQLite database (generated)
```

## ⚠️ Disclaimer

This tool is for **informational purposes only**. Requirements may vary by prefecture and individual situation. Always verify your specific requirements with:

- Your local préfecture
- [service-public.fr](https://www.service-public.fr/)
- The ANEF portal

## 📜 License

MIT License - Feel free to use and modify for your needs.

## 🤝 Contributing

Contributions are welcome! If you notice outdated information or have suggestions for improvement, please open an issue or submit a pull request.

---

<p align="center">
  Made with ❤️ for the expat community in France
</p>
