FROM mcr.microsoft.com/playwright:v1.43.0-jammy

# install python 3.10.14



RUN apt update
RUN apt-get install -y ffmpeg python3
RUN apt install python3-pip -y

RUN mkdir /app
ADD . /app
WORKDIR /app

RUN apt-get update && apt-get install -y \
    libnss3 \
    libatk-bridge2.0-0 \
    libx11-xcb1 \
    libxcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libgtk-3-0 \
    libxshmfence1 \
    libxfixes3 \
    libxext6 \
    libxrender1 \
    fonts-liberation \
    libappindicator3-1 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*


RUN pip install -r requirements.txt
RUN playwright install
RUN playwright install-deps

CMD ["python3", "main.py"]
