# Vader's Todo Empire 🌟

A dark side-inspired todo application themed around Darth Vader and the Star Wars universe. Built with Bun, Vue 3, Pinia, and enhanced with immersive sound effects and animations.

## Features

### 🎯 Core Functionality
- **Add Tasks**: Create new tasks with different priority levels
- **Complete Tasks**: Mark tasks as complete with satisfying animations
- **Edit Tasks**: Double-click to edit task text inline
- **Delete Tasks**: Remove tasks with dramatic sound effects
- **Priority System**: Organize tasks by Low, Medium, or High priority
- **Filter Tasks**: View all, active, or completed tasks
- **Advanced Sorting**: Order tasks by name, creation date, completion date, or priority
- **Smart Date Tracking**: Automatic completion date recording
- **Persistent Storage**: Tasks and preferences saved to localStorage

### 🎨 Star Wars Theme
- **Darth Vader Aesthetic**: Dark UI with red accents and Star Wars styling
- **Animated Starfield**: Moving stars background for immersion
- **Vader Helmet Logo**: Custom SVG helmet design
- **Imperial Typography**: Bold, space-themed fonts
- **Priority Indicators**: Color-coded priority levels with glowing effects

### 🔊 Sound Effects
- **Imperial March**: Plays when adding new tasks
- **Lightsaber Activation**: Sounds when completing tasks
- **Blaster Fire**: Plays when deleting tasks
- **TIE Fighter**: Sounds when activating/reactivating tasks
- **Force Power**: Dramatic sound when clearing all completed tasks

### 💬 Vader Quotes
Dynamic Darth Vader quotes throughout the app:
- "Your lack of organization is disturbing"
- "The power of the Dark Side compels you"
- "Impressive. Most impressive."
- And many more authentic Vader quotes

## Tech Stack

- **[Bun](https://bun.sh/)** - Fast JavaScript runtime and package manager
- **[Vue 3](https://vuejs.org/)** - Progressive JavaScript framework
- **[Pinia](https://pinia.vuejs.org/)** - State management for Vue
- **[Vite](https://vitejs.dev/)** - Build tool and dev server
- **[TypeScript](https://www.typescriptlang.org/)** - Type-safe JavaScript
- **Web Audio API** - For generating synthetic Star Wars sound effects

## Installation & Setup

### Prerequisites
- [Bun](https://bun.sh/docs/installation) installed on your system

### Quick Start
```bash
# Clone the project
cd vader-todo-app

# Install dependencies
bun install

# Start development server
bun run dev

# Build for production
bun run build

# Preview production build
bun run preview
```

The app will be available at `http://localhost:5173`

## Usage Guide

### Adding Tasks
1. Enter your task in the input field: "What must be accomplished, my apprentice?"
2. Select priority level (Low, Medium, High)
3. Click "Execute Order" or press Enter
4. Enjoy the Imperial March sound effect! 🎵

### Managing Tasks
- **Complete**: Click the checkbox to mark tasks as complete (lightsaber sound!)
- **Edit**: Double-click on task text to edit inline
- **Delete**: Click the lightning bolt (⚡) to destroy tasks (blaster sound!)
- **Filter**: Use the filter buttons to view different task states

### Imperial Sorting System ⚔️
Order your tasks by Imperial Decree with multiple sorting options:
- **📝 Task Name**: Alphabetical order (A-Z or Z-A)
- **📅 Creation Date**: When the task was first recorded
- **✅ Completion Date**: When tasks were marked complete
- **⚡ Priority Level**: High → Medium → Low importance

**Sorting Features:**
- Click any sort button to activate that sorting method
- Click the same button again to reverse the order (ascending ↑ or descending ↓)
- Visual indicators show current sort field and direction
- Sorting preferences are automatically saved
- Animated scan lines on active sort buttons for that Imperial feel

### Priority System
- **🔴 High Priority**: Urgent tasks that require immediate attention
- **🟠 Medium Priority**: Standard tasks for regular completion
- **🟢 Low Priority**: Tasks that can wait for the right moment

---

*"Your lack of productivity disturbs me. Use this app, you must."* - Vader (probably)

May the Force be with your task management! ⚡️
