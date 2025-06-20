# Resume-Job Analyzer & Optimizer

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()

A powerful desktop application that analyzes resumes against job descriptions and provides intelligent optimization suggestions. Built with privacy-first principles - all processing happens locally on your machine.

## 🚀 Features

- **Resume Analysis**: Upload PDF/DOCX resumes for intelligent parsing
- **Job Description Scraping**: Extract requirements from job posting URLs
- **AI-Powered Matching**: Uses spaCy NLP for semantic keyword analysis
- **Optimization Suggestions**: Get actionable recommendations to improve your resume
- **Privacy-First**: 100% local processing - no data leaves your machine
- **Cross-Platform**: Works on Windows and macOS

## 🏗️ Project Structure

```
resumefixer/
├── backend/                 # Python backend service
│   ├── src/
│   │   ├── main.py         # FastAPI server entry point
│   │   ├── api/            # API endpoints
│   │   ├── services/       # Business logic services
│   │   └── models/         # Data models
│   ├── tests/              # Backend tests
│   ├── requirements.txt    # Python dependencies
│   ├── build/              # Build scripts and configs
│   └── venv/               # Virtual environment
├── frontend/               # Desktop UI application (Tauri + React)
│   ├── src/                # UI source code
│   ├── public/             # Static assets
│   └── dist/               # Built UI assets
├── build/                  # Cross-platform build system
│   ├── docker/             # Containerized build environments
│   └── scripts/            # Platform-specific build scripts
├── docs/                   # Documentation
└── tests/                  # Integration and E2E tests
```

## 🛠️ Development Setup

### Prerequisites

- **Python 3.11+** - [Download here](https://www.python.org/downloads/)
- **Node.js 18+** - [Download here](https://nodejs.org/)
- **Rust** - [Install here](https://rustup.rs/) (for Tauri desktop app)
- **Git** - [Download here](https://git-scm.com/)
- **Docker** (optional) - [Download here](https://www.docker.com/) (for containerized builds)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/noodleA1/resumefixer.git
   cd resumefixer
   ```

2. **Run the setup script**
   ```bash
   # Windows
   .\scripts\setup.ps1
   
   # macOS/Linux
   chmod +x scripts/setup.sh
   ./scripts/setup.sh
   ```

3. **Start development**
   ```bash
   # Backend development
   cd backend
   python src/main.py
   
   # Frontend development (in another terminal)
   cd frontend
   npm run dev
   ```

## 🔧 Build System

This project uses **Nuitka** for Python compilation and **Tauri** for the desktop application shell.

### Local Development

```bash
# Backend development
cd backend
.\venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # macOS/Linux

pip install -r requirements.txt
python src/main.py
```

### Production Build

```bash
# Full cross-platform build
make build

# Platform-specific builds
make build-windows
make build-macos

# Docker builds
make docker-build
```

## 🏛️ Architecture

- **Backend**: Python FastAPI server with spaCy NLP processing
- **Frontend**: Tauri-based desktop application with React UI  
- **Communication**: Local HTTP API between frontend and backend
- **Packaging**: Nuitka for Python compilation, Tauri for app bundling
- **NLP**: spaCy with en_core_web_sm model for keyword extraction
- **Document Processing**: python-docx and pypdf for resume parsing
- **Web Scraping**: BeautifulSoup and trafilatura for job description extraction

## 🔒 Privacy & Security

- **100% Local Processing** - No data sent to external servers
- **No User Accounts** - No registration or cloud storage required
- **Your Data Stays Yours** - All resume and job data remains on your machine
- **Open Source** - Full transparency in how your data is processed

## 🚦 Project Status

This project is currently in **active development**. We're building the core architecture and testing the technical feasibility.

### Current Progress

- ✅ **SPIKE-1**: Build environment setup (Nuitka + spaCy)
- 🔄 **SPIKE-2**: spaCy compilation testing
- ⏳ **SPIKE-3**: IPC bridge development
- ⏳ **SPIKE-4**: Fallback NLP evaluation

### Roadmap

1. **Phase 1**: Core backend services (document parsing, NLP analysis)
2. **Phase 2**: Desktop UI development (Tauri + React)
3. **Phase 3**: Integration and testing
4. **Phase 4**: Cross-platform packaging and distribution

## 🤝 Contributing

We welcome contributions! This project is designed to be collaborative and educational.

### Getting Started

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and test thoroughly
4. **Commit your changes**: `git commit -m 'Add amazing feature'`
5. **Push to the branch**: `git push origin feature/amazing-feature`
6. **Open a Pull Request**

### Development Guidelines

- Follow the existing code style and structure
- Add tests for new functionality
- Update documentation as needed
- Ensure cross-platform compatibility

### Areas for Contribution

- **Backend Development**: API endpoints, NLP processing, document parsing
- **Frontend Development**: React UI components, Tauri integration
- **Testing**: Unit tests, integration tests, E2E testing
- **Documentation**: User guides, API documentation, tutorials
- **Build System**: Cross-platform packaging, CI/CD improvements

## 📚 Documentation

- **[SPIKE-1 Results](SPIKE-1-RESULTS.md)** - Build environment setup details
- **[Technical Architecture](docs/architecture.md)** - System design overview
- **[API Documentation](docs/api.md)** - Backend API reference
- **[Build Guide](docs/build.md)** - Compilation and packaging guide

## 🐛 Issues and Support

- **Bug Reports**: [Create an issue](https://github.com/noodleA1/resumefixer/issues)
- **Feature Requests**: [Start a discussion](https://github.com/noodleA1/resumefixer/discussions)
- **Questions**: Check existing issues or start a new discussion

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **spaCy** - Industrial-strength NLP library
- **FastAPI** - Modern, fast web framework for building APIs
- **Tauri** - Build smaller, faster, and more secure desktop applications
- **Nuitka** - Python compiler for standalone executables

---

**Made with ❤️ for job seekers everywhere**
