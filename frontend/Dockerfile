## Stage 1: build the Vite app
FROM node:18-alpine AS builder
WORKDIR /app

# Copy package manifests and vite/ts config to leverage cache
COPY package*.json ./
COPY package-lock.json ./
COPY tsconfig*.json ./
COPY vite.config.ts ./

# Install dependencies
RUN npm ci --silent

# Copy source and build
COPY . .
RUN npm run build

## Stage 2: serve with nginx
FROM nginx:stable-alpine

# Clear default html
RUN rm -rf /usr/share/nginx/html/*

# Copy built assets from builder
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx config (provided in repo) for SPA routing
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
