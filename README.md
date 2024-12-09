Distributed Document Summarization and Knowledge Extraction
A comprehensive system designed to summarize and extract key knowledge from documents, leveraging advanced summarization techniques and a distributed architecture. This project ensures high performance, scalability, and security while providing a user-friendly interface.

🛠️ Key Features
Client Layer:
Web Interface: For document uploads and displaying summaries.
Mobile App: Mobile access to system features.
Admin Dashboard: System monitoring and management.
API Gateway:
Load Balancing
User Authentication and Authorization
Request Rate Limiting
Application Services:
Document Management
Summarization (Extractive and Abstractive)
User Operations and Administrative Features
Processing Layer:
Multi-format Document Parsing (PDF, DOCX, TXT)
Extractive and Abstractive Summarization
Knowledge Extraction
Storage Layer:
Original Document Store
User Database
Caching Mechanisms
Summary Storage
Security:
Encrypted Data (in transit and at rest)
OAuth2/JWT Authentication
Regular Security Audits
📊 System Design Overview
High-Level Architecture

Data Flow Diagram

Sequence Diagram

Component Design
Client Layer: Interfaces for web, mobile, and admin access.
Processing Layer: Handles document parsing and summarization tasks.
Storage Layer: Secure storage for documents, summaries, and user data.
🚀 Technologies Used
Backend: RabbitMQ, RESTful APIs
Frontend: React/Flutter (as applicable)
Database: PostgreSQL, Cache Store
Security: HTTPS, AES encryption, OAuth2
⚙️ Setup and Installation
Prerequisites
Install Docker.
Install RabbitMQ.
Set up PostgreSQL for database management.
Steps
Clone the repository:
bash
Copy code
git clone https://github.com/your-repo/distributed-document-summarization.git
cd distributed-document-summarization
Build and start services using Docker Compose:
bash
Copy code
docker-compose up --build
Access the web interface at http://localhost:3000.
🧪 Usage
Upload documents via the web or mobile interface.
View generated summaries and extracted knowledge points.
Manage users and system settings via the Admin Dashboard.
📖 Documentation
For a detailed breakdown of the architecture and functionality, refer to the Project Wiki.

👥 Team
Surya Prakash Ravula
Sindhura Purnima Vempati
Svwaroopananda Kashyap
Kumarasubrahmanya Hosamane
🛡️ Security
Encrypted communication and storage.
Regular security updates and audits.
OAuth2/JWT-based authentication.

