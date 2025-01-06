# Launching the Production Version

To launch the production version of the BESSER Web Modeling Editor, follow these steps:

1. Make sure you have all dependencies installed:
```bash
npm install
```

2. Build the production version:
```bash
npm run build
```

3. The production build will be created in the `dist` folder. You can serve it using a static file server. For example:

   - Using `serve` package:
   ```bash
   npm install -g serve
   serve -s dist
   ```

   - Or using Python's built-in HTTP server:
   ```bash
   cd dist
   python -m http.server
   ```

   - Using Nginx (recommended for production):
   1. Install Nginx on your server
   2. Create or modify the Nginx configuration file (usually in `/etc/nginx/conf.d/default.conf`):
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;  # Replace with your domain

       root /path/to/your/dist;      # Replace with actual path to dist folder
       index index.html;

       location / {
           try_files $uri $uri/ /index.html;  # For SPA routing
       }

       # Optional: Enable gzip compression
       gzip on;
       gzip_types text/plain text/css application/javascript;
   }
   ```
   3. Test and restart Nginx:
   ```bash
   sudo nginx -t
   sudo systemctl restart nginx
   ```

   - Using Docker with Nginx (recommended for containerized deployment):
   1. Build the Docker image:
   ```bash
   docker build -t besser-web-editor .
   ```
   
   2. Run the container:
   ```bash
   docker run -d -p 80:80 besser-web-editor
   ```

   3. Access the application at http://localhost

4. Access the application through your web browser:
   - For `serve`: http://localhost:3000
   - For Python server: http://localhost:8000
   - For Nginx: http://your-domain.com or http://localhost

Note: Make sure all environment variables are properly set for production before building.
