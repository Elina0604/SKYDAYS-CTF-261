# Coding Agents Guide - Brooklyn 99 Heist CTF Project

This document provides guidance for coding agents working on this React TypeScript CTF (Capture The Flag) educational project.

## Project Overview

This is a **React 19 + TypeScript** educational CTF application themed around Brooklyn Nine-Nine, designed to teach web security vulnerabilities around client-side encryption and authentication. The project uses **Vite** as the build tool and **Bun** as the package manager.

## Build/Lint/Test Commands

### Primary Commands (Bun - Recommended)
```bash
# Development server (starts on port 3000)
bun dev

# Production build
bun build

# Linting
bun lint

# Preview production build
bun preview
```

### Alternative Commands (npm/yarn)
```bash
# Development server
npm run dev / yarn dev

# Production build  
npm run build / yarn build

# Linting
npm run lint / yarn lint

# Preview production build
npm run preview / yarn preview
```

### Build Process Details
- **TypeScript compilation:** `tsc -b` (type checking)
- **Bundle creation:** `vite build` (with Terser minification)
- **Output directory:** `dist/`
- **Source maps:** Disabled in production builds

### Testing
⚠️ **No testing framework is currently configured.** To add testing:
- Consider **Vitest** for unit tests (pairs well with Vite)
- Add test scripts to `package.json`
- Create `__tests__` directories or `.test.ts/.spec.ts` files

## Code Style Guidelines

### Import Conventions
```typescript
// React imports first
import React, { useState } from 'react';
import { createRoot } from 'react-dom/client';

// Third-party libraries
import CryptoJS from 'crypto-js';

// Local imports (relative paths)
import { LOGIN_CONFIG, CHARACTERS } from '../constants/config';
import './ComponentName.css';
```

### File Organization
```
src/
├── components/         # React components (.tsx)
├── utils/             # Utility functions (.ts)
├── constants/         # Configuration and constants (.ts)
├── assets/           # Static assets (images, etc.)
└── *.css            # Component-specific stylesheets
```

### TypeScript Configuration
- **Target:** ES2022
- **Module:** ESNext with bundler resolution
- **Strict mode:** Enabled
- **JSX:** react-jsx (React 17+ transform)
- **Key compiler options:**
  - `noUnusedLocals: true`
  - `noUnusedParameters: true`
  - `noFallthroughCasesInSwitch: true`
  - `verbatimModuleSyntax: true`

### Component Structure
```typescript
interface ComponentProps {
  onAction: () => void;
  data?: string;
}

const ComponentName: React.FC<ComponentProps> = ({ onAction, data }) => {
  const [state, setState] = useState<string>('');
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Handler logic
  };

  return (
    <div className="component-name">
      {/* JSX content */}
    </div>
  );
};

export default ComponentName;
```

### Naming Conventions
- **Components:** PascalCase (`Login.tsx`, `Dashboard.tsx`)
- **Files:** PascalCase for components, camelCase for utilities
- **Variables/Functions:** camelCase (`isAuthenticated`, `handleSubmit`)
- **Constants:** UPPER_SNAKE_CASE (`LOGIN_CONFIG`, `ERROR_MESSAGES`)
- **CSS Classes:** kebab-case (`login-container`, `submit-btn`)
- **Interfaces:** PascalCase with descriptive suffixes (`LoginProps`, `SecurityConfig`)

### Error Handling Patterns
```typescript
// Async operations with try-catch
const processData = async (input: string): Promise<string> => {
  try {
    const result = await someAsyncOperation(input);
    return result;
  } catch (error) {
    console.error('Processing failed:', error);
    return '';
  }
};

// Form validation with state
const [error, setError] = useState('');

const handleSubmit = (e: React.FormEvent) => {
  e.preventDefault();
  setError('');
  
  if (!isValid(input)) {
    setError(ERROR_MESSAGES.VALIDATION_ERROR);
    return;
  }
};
```

### State Management Patterns
- Use `useState` for local component state
- Prefer controlled components for forms
- Pass callbacks via props for parent-child communication
- Use descriptive state variable names

```typescript
const [isAuthenticated, setIsAuthenticated] = useState(false);
const [loading, setLoading] = useState(false);
const [password, setPassword] = useState('');
```

## ESLint Configuration

The project uses **ESLint 9** with flat config format:

### Enabled Rules
- **@eslint/js recommended** - Core JavaScript linting
- **typescript-eslint recommended** - TypeScript-specific rules
- **react-hooks recommended** - React hooks linting
- **react-refresh** - Vite HMR compatibility

### Target Files
- `**/*.{ts,tsx}` - TypeScript and TSX files only
- **Ignored:** `dist/` directory

## Project-Specific Guidelines

### Security Context (CTF Educational Purpose)
This project **intentionally contains security vulnerabilities** for educational purposes:
- Client-side password validation
- Exposed encryption keys in global scope
- Base64-encoded "secrets" in source code

**When working on this project:**
- ⚠️ **DO NOT fix the intentional vulnerabilities**
- Maintain the educational CTF structure
- Keep security flaws visible for learning purposes
- Add comments to explain why code is insecure (for educational value)

### Theme and Styling
- **Brooklyn 99 theme** - Keep consistent with TV show references
- **YTÜ (Yıldız Technical University) branding** - Maintain Turkish university context
- **Color scheme:** Navy blue (#1d3b6c), Gold (#ffcc00), Hacker green (#00ff00)
- Use **CSS files** for styling (no CSS-in-JS currently used)

### Console Logging Patterns
```typescript
// Educational feedback patterns used in the project
console.log('🎉 Welcome to the 99th Precinct! Phase 1 Complete.');
console.log('🔍 Jake: Hmm, sistem biraz yavaş çalışıyor bugün.');
console.error('Decryption failed:', error);
```

### Character Integration
When adding features, maintain character consistency:
- **Boyle:** Food/pizza references, overly enthusiastic about security
- **Jake:** Cool/casual attitude, detective work metaphors
- **Holt:** Formal, precise language
- **Terry:** Third-person references, yogurt mentions

## Development Workflow

1. **Start development server:** `bun dev`
2. **Make changes** to source files in `src/`
3. **Check types:** Automatic in IDE, or `bun build` for full check
4. **Lint code:** `bun lint` (auto-fix with `bun lint --fix`)
5. **Test build:** `bun build` before committing
6. **Preview:** `bun preview` to test production build locally

## Docker Support

The project includes Docker configuration:
- **Development:** Use local Bun/npm commands
- **Production:** Multi-stage Docker build with nginx
- **Port:** 3000 (development), 80 (production container)

---

**Remember:** This is an educational CTF project. Maintain the balance between clean code practices and intentional security vulnerabilities that serve the learning objectives.