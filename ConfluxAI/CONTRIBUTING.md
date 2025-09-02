# Contributing to ConfluxAI

Thank you for your interest in contributing to ConfluxAI! This document provides guidelines and information for contributors.

## 🎯 How to Contribute

### Reporting Issues

- Use the [GitHub Issues](https://github.com/kasimlohar/kurukshetra/issues) page
- Search existing issues before creating a new one
- Provide detailed information about the bug or feature request
- Include steps to reproduce for bugs
- Add relevant labels

### Code Contributions

1. **Fork the Repository**
   ```bash
   git fork https://github.com/kasimlohar/kurukshetra.git
   cd kurukshetra/ConfluxAI
   ```

2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Your Changes**
   - Follow the coding standards below
   - Write tests for new functionality
   - Update documentation as needed

4. **Test Your Changes**
   ```bash
   npm run check          # TypeScript type checking
   npm run build          # Ensure build works
   npm run dev            # Test locally
   ```

5. **Commit Your Changes**
   ```bash
   git commit -m "feat: add amazing new feature"
   ```

6. **Push and Create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

## 📝 Coding Standards

### TypeScript Guidelines

- Use TypeScript for all new code
- Define proper types and interfaces
- Avoid `any` types when possible
- Use strict TypeScript configuration

### Code Style

- Use 2 spaces for indentation
- Use semicolons
- Use single quotes for strings
- Use meaningful variable and function names
- Add JSDoc comments for complex functions

### React Guidelines

- Use functional components with hooks
- Use TypeScript for prop types
- Follow React best practices
- Use proper error boundaries

### File Organization

```
src/
├── components/          # Reusable UI components
│   ├── ui/             # Basic UI components (buttons, inputs, etc.)
│   └── [Component]/    # Feature-specific components
├── pages/              # Page components
├── hooks/              # Custom React hooks
├── lib/                # Utility functions
└── types/              # TypeScript type definitions
```

## 🔧 Development Setup

### Prerequisites

- Node.js 18+
- npm or yarn
- Git

### Setup Steps

1. **Clone and Install**
   ```bash
   git clone https://github.com/kasimlohar/kurukshetra.git
   cd kurukshetra/ConfluxAI
   npm install
   ```

2. **Environment Setup**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start Development**
   ```bash
   npm run dev
   ```

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run check` - TypeScript type checking
- `npm run dev:vercel` - Start Vercel-compatible dev server

## 📋 Pull Request Guidelines

### Before Submitting

- [ ] Code follows the style guidelines
- [ ] Self-review of the code
- [ ] Commented hard-to-understand areas
- [ ] Made corresponding changes to documentation
- [ ] Changes generate no new warnings
- [ ] Added tests that prove the fix/feature works
- [ ] New and existing tests pass locally

### PR Description Template

```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Tested locally
- [ ] Added new tests
- [ ] All tests pass

## Screenshots (if applicable)
Add screenshots to help explain your changes.

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
```

## 🐛 Bug Reports

When reporting bugs, please include:

- **Description**: Clear description of the bug
- **Steps to Reproduce**: Detailed steps to reproduce the issue
- **Expected Behavior**: What you expected to happen
- **Actual Behavior**: What actually happened
- **Environment**: OS, browser, Node.js version, etc.
- **Screenshots**: If applicable
- **Additional Context**: Any other relevant information

## 💡 Feature Requests

When requesting features, please include:

- **Problem Description**: What problem does this solve?
- **Proposed Solution**: How should this feature work?
- **Alternatives Considered**: Other solutions you've considered
- **Additional Context**: Any other relevant information

## 🎨 Design Guidelines

### UI/UX Principles

- **Consistency**: Follow existing design patterns
- **Accessibility**: Ensure features are accessible
- **Responsiveness**: Support mobile and desktop
- **Performance**: Optimize for speed and efficiency

### Component Design

- Use shadcn/ui components when possible
- Follow Radix UI accessibility guidelines
- Implement proper keyboard navigation
- Add loading states and error handling

## 📚 Documentation

### Code Documentation

- Add JSDoc comments for complex functions
- Include usage examples in README
- Document API endpoints
- Update type definitions

### README Updates

When adding features, update:
- Features section
- Installation instructions
- Usage examples
- Configuration options

## 🧪 Testing Guidelines

### Types of Tests

- **Unit Tests**: Test individual functions/components
- **Integration Tests**: Test feature workflows
- **E2E Tests**: Test complete user journeys

### Testing Tools

- Jest for unit testing
- React Testing Library for component testing
- Playwright for E2E testing (future)

## 🔍 Code Review Process

### What We Look For

- Code quality and maintainability
- Performance implications
- Security considerations
- Testing coverage
- Documentation updates

### Review Timeline

- Initial review within 48 hours
- Follow-up reviews within 24 hours
- Merge after approval from maintainers

## 🚀 Release Process

### Versioning

We use [Semantic Versioning](https://semver.org/):
- **Major**: Breaking changes
- **Minor**: New features
- **Patch**: Bug fixes

### Release Steps

1. Update version in package.json
2. Update CHANGELOG.md
3. Create release tag
4. Deploy to production

## 📞 Getting Help

- **GitHub Discussions**: For questions and discussions
- **GitHub Issues**: For bugs and feature requests
- **Email**: kasimlohar@example.com for direct contact

## 🙏 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Special thanks in major releases

Thank you for contributing to ConfluxAI! 🎉
