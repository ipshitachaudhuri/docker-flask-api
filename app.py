name: Deploy Flask API

on:
  workflow_run:
    workflows:
      - Build and Push Flask API
    types:
      - completed

jobs:
  deploy:

    if: ${{ github.event.workflow_run.conclusion == 'success' }}

    runs-on: ubuntu-latest

    steps:

      - name: Deploy to EC2
        uses: appleboy/ssh-action@v1.0.3

        with:
          host: ${{ secrets.EC2_HOST }}
          username: ${{ secrets.EC2_USERNAME }}
          key: ${{ secrets.EC2_SSH_KEY }}

          script: |

            set -e

            mkdir -p ~/flask-api
            cd ~/flask-api


            cat > docker-compose.yml <<EOF

            services:

              postgres-db:
                image: postgres:16
                container_name: postgres-db
                restart: unless-stopped

                environment:
                  POSTGRES_DB: postgres
                  POSTGRES_USER: postgres
                  POSTGRES_PASSWORD: postgres

                volumes:
                  - postgres-data:/var/lib/postgresql/data

                networks:
                  - flask-network


              flask-api:

                image: ghcr.io/ipshitachaudhuri/flask-api:${{ github.event.workflow_run.head_sha }}

                container_name: flask-api

                restart: unless-stopped

                ports:
                  - "8000:8000"

                environment:

                  DB_HOST: postgres-db
                  DB_NAME: postgres
                  DB_USER: postgres
                  DB_PASSWORD: postgres


                depends_on:
                  postgres-db:
                    condition: service_healthy


                networks:
                  - flask-network


            volumes:

              postgres-data:


            networks:

              flask-network:

            EOF


            docker compose pull

            docker compose up -d --force-recreate --remove-orphans

            docker compose ps

            curl localhost:8000/health

