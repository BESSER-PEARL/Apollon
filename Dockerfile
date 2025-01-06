# Build stage
FROM node:20-alpine AS build-stage
WORKDIR /app

# Set environment to production
ENV NODE_ENV=production

# Install dependencies first (better layer caching)
COPY package*.json ./
COPY tsconfig*.json ./
COPY webpack ./webpack
RUN npm install --legacy-peer-deps --ignore-scripts --production

# Copy source files
COPY . .

# Build TypeScript files if needed
RUN npm run prepare:full || true

# Build the application
RUN npm run build

# Production stage
FROM nginx:stable-alpine
COPY --from=build-stage /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]