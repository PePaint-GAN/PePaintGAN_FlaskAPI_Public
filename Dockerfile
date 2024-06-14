FROM python:3.11

WORKDIR /code

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
    
COPY . .

EXPOSE 50505

ENTRYPOINT [ "gunicorn", "app:app" ]