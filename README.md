# MoodieFlix 🍿

“Let your mood pick the movie.”

An AI-powered, natural language movie recommendation system that understands your mood and suggests perfect movies to watch. Built with **Streamlit** and **OpenRouter LLMs**.

## ✨ Features

- 🎬 **Natural Language Processing** - Describe what you want to watch in plain English
- 🤖 **AI-Powered Recommendations** - Powered by OpenRouter's GPT-3.5 Turbo
- 🎨 **Modern UI Design** - Sleek glass-morphism cards with cinematic styling
- 📱 **Responsive Layout** - Works beautifully on desktop and mobile
- 🔒 **Secure API Management** - Environment-based API key handling

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- OpenRouter API key ([Get one here](https://openrouter.ai/))

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/aakritidhardubey/MoodieFlix.git
   cd moodieflix
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API key**
   
   Create `.streamlit/secrets.toml`:
   ```toml
   OPENROUTER_API_KEY = "your_openrouter_api_key_here"
   ```

4. **Add background image (optional)**
   
   Place your background image in the project root with one of these names:
   - `image2.jpg`
   - `image2.png`
   - `background.jpg`
   - `background.png`

5. **Run the app**
   ```bash
   streamlit run app.py
   ```

## 📦 Dependencies

```txt
streamlit>=1.28.0
requests>=2.31.0
```

## 🎯 Usage

1. **Launch the app** - Run `streamlit run app.py`
2. **Describe your mood** - Type what you want to watch (e.g., "romantic comedy with strong female lead")
3. **Get recommendations** - Receive personalized movie suggestions in beautiful cards
4. **Explore more** - Try different moods and genres for varied recommendations

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👩‍💻 Author

**Aakriti Dhar Dubey**
- 📧 Email: aakriti2144@gmail.com

