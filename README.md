# ChefPanda

ChefPanda is a hands-free cooking companion that transforms YouTube cooking tutorials into easy-to-follow, gesture-controlled recipes. Say goodbye to touching your screen with messy hands while cooking!

## 🌟 Features

- **YouTube Integration**
  - Automatically scrapes cooking videos and transcripts
  - Supports searching by URL, channel, or keywords
  - Intelligent recipe extraction from video content

- **Hands-Free Cooking Mode**
  - Step-by-step recipe navigation using gestures
  - Progress tracking while cooking
  - Video reference integration
  - Touch fallback controls

- **Smart Recipe Management**
  - Personalized recipe recommendations
  - Save favorite recipes
  - Dietary restrictions handling
  - Search and filter functionality

## 🛠️ Technical Stack

### Backend
- Python 3.8+
- FastAPI
- MongoDB with mongoengine ODM
- YouTube Data API v3
- YouTube Transcript API
- pytest for testing

### Frontend
- Next.js 13+
- React 18+
- TailwindCSS
- React Testing Library

### Deployment
- Vercel (Frontend)
- Cloud hosting (Backend)

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Node.js and npm
- MongoDB
- YouTube API credentials

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/chefpanda.git
cd chefpanda
```

2. Set up the backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up the frontend
```bash
cd frontend
npm install
```

4. Configure environment variables
```bash
# Backend (.env)
YOUTUBE_API_KEY=your_api_key
MONGODB_URI=your_mongodb_uri

# Frontend (.env.local)
NEXT_PUBLIC_API_URL=http://localhost:8000
```

5. Start the development servers
```bash
# Backend
cd backend
uvicorn main:app --reload

# Frontend (in another terminal)
cd frontend
npm run dev
```

## 📝 Project Structure

```
chefpanda/
├── backend/
│   ├── youtube_parser/     # YouTube scraping and parsing
│   ├── recipe_gen/        # Recipe generation service
│   └── api/              # FastAPI endpoints
├── frontend/
│   ├── components/       # React components
│   ├── pages/           # Next.js pages
│   └── styles/          # TailwindCSS styles
└── docs/               # Documentation
```

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- YouTube Data API
- YouTube Transcript API
- All the amazing cooking content creators

## 🔮 Future Enhancements

- Advanced gesture recognition
- Voice command support
- Social features (sharing, rating)
- ML-based recipe recommendations
- Mobile app version

---

Made with ❤️ for home cooks everywhere