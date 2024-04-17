## This is the repository for our project: Husky Leagues
By Dylan Weinmann, Arinjay Singh, Kenneth Aldridge, Aarav Shyamkumar

The application is a comprehensive platform designed to streamline the experience of participating in and following recreational sports leagues at Northeastern University. Catering to a diverse user base that includes team members, fans, referees, sponsors, and administrators, it serves the primary purpose of making recreational sports leagues more organized and accessible for everyone involved. Fans can easily follow their friends, their friends’ teams, or any sport that piques their interest. The application boasts a rich repository of game histories, showcasing team records and championship titles across all sports, enhancing the engagement and connection of the university's sports community. Moreover, it facilitates local businesses in sponsoring teams, thereby fostering a strong link between the university and the local business ecosystem. A central feature of the application is its comprehensive game details section, which provides essential information on facilities, schedules, and contact details for each party involved, ensuring a seamless and integrated sports league experience at Northeastern.

# MySQL + Flask Boilerplate Project

This repo contains a boilerplate setup for spinning up 3 Docker containers: 
1. A MySQL 8 container for obvious reasons
1. A Python Flask container to implement a REST API
1. A Local AppSmith Server

## How to setup and start the containers
**Important** - you need Docker Desktop installed

1. Clone this repository.  
1. Create a file named `db_root_password.txt` in the `secrets/` folder and put inside of it the root password for MySQL. 
1. Create a file named `db_password.txt` in the `secrets/` folder and put inside of it the password you want to use for the a non-root user named webapp. 
1. In a terminal or command prompt, navigate to the folder with the `docker-compose.yml` file.  
1. Build the images with `docker compose build`
1. Start the containers with `docker compose up`.  To run in detached mode, run `docker compose up -d`. 




