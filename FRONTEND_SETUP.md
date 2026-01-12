# Frontend Setup Instructions

## Prerequisites

Install Node.js and npm:

```bash
# Install Node.js 18+
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify installation
node --version
npm --version
```

## Setup Frontend

1. Navigate to frontend directory:
```bash
cd /home/ubuntu/PayCoreX/frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create environment file:
```bash
echo "VITE_API_URL=https://api.buildforu.pw" > .env
```

4. Run development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Production Build

1. Build for production:
```bash
npm run build
```

2. Serve with Nginx:
```bash
# Copy build files to Nginx
sudo cp -r dist/* /var/www/paycorex/

# Or serve from frontend/dist
```

## Nginx Configuration for Frontend

Add to your Nginx config:

```nginx
server {
    listen 80;
    server_name buildforu.pw www.buildforu.pw;
    
    root /home/ubuntu/PayCoreX/frontend/dist;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location /api {
        proxy_pass https://api.buildforu.pw;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Access Dashboard

- Development: `http://localhost:3000`
- Production: `https://buildforu.pw` (after Nginx setup)

