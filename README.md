---

```markdown
# 🎮 sajilopygame

`sajilopygame` is a beginner-friendly Python library built on top of `pygame`, designed to make 2D game development easy and accessible for students and hobbyists. With simple functions to load characters, handle movement, and update the game window, `sajilopygame` lets you focus on building games — not boilerplate code.

---

## 📦 Installation

You must have Python and `pygame` installed. If not:

```bash
pip install pygame
```

Then, clone this repository or copy the `sajilopygame.py` file into your project folder.

---

## 🛠️ Getting Started

Here's a minimal example to get your first game up and running:

```python
from sajilopygame import sajilopygame

game = sajilopygame()

game.window_title("My First Game")
game.favicon("icon.png")
game.background_color((0, 0, 0))

game.create_player("player.png")
game.assign_lr_keys()
game.bound_player_to_window()

while True:
    game.refresh_window()
    game.load_player()
```

---

## 🚀 Features

- 🖼️ Load background image or color
- 🕹️ Move players/objects using arrow keys
- 👾 Add players, enemies, and other objects
- 📏 Get and update positions of objects
- 🔒 Restrict movement within the screen
- 🔁 Simple game loop with built-in quit handling

---

## 📘 Documentation

Full documentation is available in the [GitHub Wiki](https://github.com/SudipVikram/sajilopygame/wiki).  
Start with the [Function Descriptions](https://github.com/SudipVikram/sajilopygame/wiki/Function-Descriptions) page.

---

## 📂 Folder Structure

```
your-project/
│
├── main.py                # Your game logic
├── sajilopygame.py        # The library
├── assets/
│   ├── player.png
│   └── icon.png
```

---

## 🙋‍♂️ Why use sajilopygame?

- 🧒 Made for beginners in Python
- 🧼 Clean abstraction over Pygame
- 🧠 Easy to learn, quick to prototype
- 🎓 Perfect for classrooms and workshops

---

## 📄 License

This project is licensed under the MIT License.  
See the [LICENSE](LICENSE) file for details.

---

## ❤️ Contributing

Pull requests are welcome!  
Feel free to open issues for bug reports or feature suggestions.

---

## 🧠 Author

Made with ❤️ by [Sudip Vikram](https://github.com/SudipVikram)
```

---
