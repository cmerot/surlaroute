# Stage 0, "build-stage", based on Node.js, to build and compile the frontend
FROM node:20 AS build-stage

WORKDIR /app

COPY package*.json /app/

COPY ./ /app/

RUN npm install

RUN npm run build

ARG VITE_API_URL=${VITE_API_URL}


# Stage 1, based on node
FROM node:20
WORKDIR /app
COPY --from=build-stage /app/build/ build/
COPY package.json .
EXPOSE 5174
ENV NODE_ENV=production

CMD ["node", "build"]
