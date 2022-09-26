#
# React builder image
#
FROM node:16.17-alpine AS react-builder

RUN mkdir -p /build
WORKDIR /build

# install node modules
COPY client/package.json ./
RUN yarn install

# build the app
COPY client .
RUN yarn build

#
# Target image
#
FROM python:3.9-slim AS target

RUN mkdir -p /app
WORKDIR /app

# python settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install dependencies
COPY server/requirements.txt . 
COPY server/migrate.sh . 
RUN python -m pip install --no-cache-dir -r requirements.txt
RUN chmod +x migrate.sh

# copy the server app and cleint buld output
COPY server .
COPY --from=react-builder /build/build ./build

# django port
EXPOSE 8000

# collect static into single folder
RUN python manage.py collectstatic --noinput

# serving django with gunicorn on port 8000 (timeout 60 seconds)
CMD ["gunicorn", "-b", "0.0.0.0:8000", "-t", "60", "core.wsgi"]