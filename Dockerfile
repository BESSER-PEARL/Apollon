FROM node:18.20.4

WORKDIR /app

# Copy package files
COPY package*.json ./

# Disable husky completely
ENV HUSKY=0
ENV DISABLE_HUSKY=1
ENV CI=true

# Copy the rest of the application code
COPY . .

# Install dependencies without running scripts
RUN npm install --ignore-scripts

# Build the production version
RUN npm run build

# Expose the port the app runs on
EXPOSE 8080

# Install a simple HTTP server for serving static files
RUN npm install -g http-server

# Start the server pointing to the dist directory
CMD ["http-server", "dist", "-p", "8080"]