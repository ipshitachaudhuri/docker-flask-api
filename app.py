name: Docker Build

on:
  push:
    branches:
      - main

jobs:
  build:

    runs-on: ubuntu-latest

    permissions:
      contents: read
      packages: write

    steps:

      - name: Checkout code
        uses: actions/checkout@v4


      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"


      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest


      - name: Run tests
        run: |
          pytest


      - name: Login to GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}


      - name: Build Docker image
        run: |
          docker build \
          -t ghcr.io/ipshitachaudhuri/flask-api:${{ github.sha }} .


      - name: Push Docker image
        run: |
          docker push ghcr.io/ipshitachaudhuri/flask-api:${{ github.sha }}

