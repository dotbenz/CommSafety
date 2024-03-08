# CommSafety
##Community Safety Application
Overview
**CommSafety** is a web-based application designed to facilitate the reporting and tracking of criminal incidents within a community. The application allows users to submit reports of criminal activities anonymously, view reported incidents on a map, and stay informed about safety concerns in their area. It aims to empower communities by providing a platform for sharing information and collaborating with law enforcement agencies to improve safety and security.

**Features**
**Anonymous Reporting**: Users can submit reports of criminal incidents without revealing their identity, ensuring confidentiality and encouraging participation.
**Interactive Map**: The application provides an interactive map interface where users can visualize reported incidents and filter them based on various criteria such as location, type of crime, and date.
**Real-time Updates**: Reported incidents are displayed in real-time on the map, allowing users to stay informed about recent events in their area.
**User Authentication**: Registered users can create accounts to access additional features such as saving favorite locations, receiving personalized alerts, and contributing to community discussions.
**Admin Panel**: Administrators have access to an admin panel where they can manage reported incidents, moderate user-generated content, and communicate with users. <br/>
**Technologies Used**
Frontend: HTML, CSS, JavaScript, Bootstrap
Backend: Django (Python)
Database: SQLite
Mapping: Leaflet.js, OpenStreetMap
Authentication: Django Authentication System
Notifications: Django Signals, Email/Text Notifications API
Deployment: AWS EC2

**Installation and Setup**
1. Clone Repository
   git clone https://github.com/dotbenz/CommSafety.git
2. Install Dependencies
   cd CommSafety
   pip install -r requirements.txt
3. Set-up Database
   python manage.py migrate
4. Start the Development Server
   python manage.py runserver
5. Access the application at http://localhost:8000 in your web browser.

**VISIT WEB APPLICATION ON AWS EC2**
https://bit.ly/komsafety


**Usage**
Sign up for an account or log in if you already have one.
Explore the map to view reported incidents in your area.
Use the search functionality to find incidents by location or type of crime.
Submit a report if you witness a criminal activity or safety concern.
Stay informed about safety alerts and community initiatives through notifications.

**License**
This project is licensed under the MIT License.

**Contact**
For questions or inquiries about the Crime Reporting App, please contact dotbenzer@gmail.com.

