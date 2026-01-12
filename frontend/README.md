# PayCoreX Dashboard Frontend

Professional payment gateway dashboard built with React and Tailwind CSS.

## 🚀 Quick Start

### Local Development

```bash
# Install dependencies
npm install

# Set environment variable
echo "VITE_API_URL=https://api.paycorex.dev" > .env

# Run development server
npm run dev
```

### Build for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

## 📦 Tech Stack

- **React 18** - UI library
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **React Router** - Routing
- **Axios** - HTTP client
- **Heroicons** - Icons

## 🌐 Deployment

### Deploy to Vercel

1. Push code to GitHub
2. Import project in Vercel
3. Set root directory to `frontend`
4. Add environment variable: `VITE_API_URL=https://api.paycorex.dev`
5. Deploy!

See `VERCEL_DEPLOYMENT.md` for detailed instructions.

## ⚙️ Environment Variables

- `VITE_API_URL` - Backend API URL (required)

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/    # Reusable components
│   ├── pages/         # Page components
│   ├── services/      # API services
│   ├── context/       # React context
│   └── utils/         # Utility functions
├── public/            # Static assets
└── package.json       # Dependencies
```

## 🔗 Links

- **Production API**: https://api.paycorex.dev
- **Documentation**: https://api.paycorex.dev/docs
