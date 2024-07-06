FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create the entrypoint script
RUN echo '#!/bin/sh' > /entrypoint.sh
RUN echo 'python manage.py migrate' >> /entrypoint.sh
RUN echo 'python manage.py runserver 0.0.0.0:8000' >> /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
